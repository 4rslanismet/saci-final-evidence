# frozen_string_literal: true

require "json"

Vagrant.require_version ">= 2.4.0"

ROOT = File.expand_path(__dir__)
LAB_DIR = File.join(ROOT, "lab")
TOPOLOGY_PATH = File.join(LAB_DIR, "topology.json")
TOPOLOGY = JSON.parse(File.read(TOPOLOGY_PATH, encoding: "UTF-8"))

profile = ENV.fetch("SACI_LAB_PROFILE", "evidence").downcase
network_mode = ENV.fetch("SACI_NETWORK_MODE", "static").downcase
deploy_services = ENV.fetch("SACI_DEPLOY_SERVICES", "0") == "1"

profiles = {
  "evidence" => ["wsiem"],
  "portable" => TOPOLOGY.fetch("machines").keys,
  "native" => TOPOLOGY.fetch("machines").keys
}.freeze

unless profiles.key?(profile)
  raise "Unknown SACI_LAB_PROFILE=#{profile.inspect}. Use evidence, portable, or native."
end

unless %w[dhcp static].include?(network_mode)
  raise "Unknown SACI_NETWORK_MODE=#{network_mode.inspect}. Use dhcp or static."
end

linux_box = ENV.fetch("SACI_LINUX_BOX", TOPOLOGY.dig("boxes", "linux", "name"))
linux_box_version = ENV.fetch(
  "SACI_LINUX_BOX_VERSION",
  TOPOLOGY.dig("boxes", "linux", "version").to_s
)


def provider_tuning(machine, name, spec)
  memory = Integer(spec.fetch("memory_mb"))
  cpus = Integer(spec.fetch("cpus"))
  display_name = "saci-#{name}"

  machine.vm.provider "virtualbox" do |provider|
    provider.name = display_name
    provider.memory = memory
    provider.cpus = cpus
  end

  machine.vm.provider "vmware_desktop" do |provider|
    provider.vmx["displayName"] = display_name
    provider.vmx["memsize"] = memory.to_s
    provider.vmx["numvcpus"] = cpus.to_s
  end

  machine.vm.provider "hyperv" do |provider|
    provider.vmname = display_name
    provider.memory = memory
    provider.maxmemory = memory
    provider.cpus = cpus
    provider.enable_automatic_checkpoints = false
  end

  machine.vm.provider "libvirt" do |provider|
    provider.title = display_name
    provider.memory = memory
    provider.cpus = cpus
  end

  # ESXi credentials are intentionally read only when the provider is selected.
  # No password or API secret is stored in the repository.
  machine.vm.provider :vmware_esxi do |provider|
    provider.esxi_host = ENV.fetch("GOAD_VAGRANT_ESXIHOST")
    provider.esxi_user = ENV.fetch("GOAD_VAGRANT_ESXIUSER", "root")
    provider.esxi_password = ENV.fetch("GOAD_VAGRANT_ESXIPASSWORD")
    provider.esxi_datastore = ENV.fetch("GOAD_VAGRANT_ESXIDATASTORE", "datastore1")
    provider.esxi_virtual_network = [ENV.fetch("GOAD_VAGRANT_ESXINETWORK", "SOC_VLAN")]
    provider.guest_memsize = memory
    provider.guest_numvcpus = cpus
  end

  machine.vm.provider("parallels") { |_provider| }
  machine.vm.provider("qemu") { |_provider| }
end

Vagrant.configure("2") do |config|
  config.vm.box_check_update = false
  config.vm.boot_timeout = 1_200
  config.vm.graceful_halt_timeout = 120
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.ssh.keep_alive = true

  profiles.fetch(profile).each do |name|
    spec = TOPOLOGY.fetch("machines").fetch(name)
    guest = profile == "native" ? spec.fetch("native_guest") : "linux"

    config.vm.define name, primary: name == "wsiem" do |machine|
      machine.vm.hostname = name

      if guest == "linux"
        machine.vm.box = linux_box
        machine.vm.box_version = linux_box_version unless linux_box_version.empty?
      else
        box_env = "SACI_#{name.upcase.gsub('-', '_')}_BOX"
        box_version_env = "#{box_env}_VERSION"
        box = ENV[box_env]
        if box.to_s.empty?
          raise "Native profile requires #{box_env} with a provider-compatible #{guest} box."
        end
        machine.vm.box = box
        machine.vm.box_version = ENV[box_version_env] unless ENV[box_version_env].to_s.empty?
      end

      if network_mode == "static"
        machine.vm.network "private_network", ip: spec.fetch("historical_ip")
      else
        machine.vm.network "private_network", type: "dhcp"
      end

      spec.fetch("forwarded_ports", {}).each do |label, ports|
        machine.vm.network "forwarded_port",
          guest: Integer(ports.fetch("guest")),
          host: Integer(ports.fetch("host")),
          host_ip: "127.0.0.1",
          id: "#{name}-#{label}",
          auto_correct: true
      end

      provider_tuning(machine, name, spec)

      if guest == "windows"
        machine.vm.communicator = "winrm"
        machine.vm.provision "file", source: TOPOLOGY_PATH, destination: "C:/Windows/Temp/saci-topology.json"
        machine.vm.provision "shell",
          path: File.join(LAB_DIR, "provision", "windows.ps1"),
          args: [name, spec.fetch("asset_id"), spec.fetch("role"), profile]
      elsif guest == "freebsd"
        machine.vm.provision "file", source: TOPOLOGY_PATH, destination: "/tmp/saci-topology.json"
        machine.vm.provision "shell",
          path: File.join(LAB_DIR, "provision", "freebsd.sh"),
          args: [name, spec.fetch("asset_id"), spec.fetch("role"), profile]
      else
        machine.vm.provision "file", source: TOPOLOGY_PATH, destination: "/tmp/saci-topology.json"
        machine.vm.provision "shell",
          path: File.join(LAB_DIR, "provision", "common.sh"),
          args: [name, spec.fetch("asset_id"), spec.fetch("role"), profile]

        if deploy_services && %w[wsiem cti01].include?(name)
          machine.vm.provision "shell", path: File.join(LAB_DIR, "provision", "install_docker.sh")
        end

        if name == "wsiem"
          machine.vm.provision "file",
            source: File.join(ROOT, "docs", "data", "final"),
            destination: "/tmp/saci-final"
          machine.vm.provision "file",
            source: File.join(LAB_DIR, "verify.py"),
            destination: "/tmp/saci-verify.py"
          machine.vm.provision "shell",
            path: File.join(LAB_DIR, "provision", "wsiem.sh"),
            args: [
              profile,
              TOPOLOGY.dig("versions", "wazuh"),
              TOPOLOGY.dig("versions", "wazuh_docker_ref"),
              deploy_services ? "1" : "0"
            ]
        elsif name == "cti01"
          machine.vm.provision "shell",
            path: File.join(LAB_DIR, "provision", "cti01.sh"),
            args: [
              profile,
              TOPOLOGY.dig("versions", "misp_docker_ref"),
              deploy_services ? "1" : "0"
            ]
        else
          machine.vm.provision "shell",
            path: File.join(LAB_DIR, "provision", "role_stub.sh"),
            args: [name, spec.fetch("asset_id"), spec.fetch("role"), profile]
        end
      end
    end
  end
end
