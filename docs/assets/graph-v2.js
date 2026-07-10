(function () {
  "use strict";

  const palette = {
    asset: "#43b8bb",
    log_source: "#6b9db9",
    control: "#72b686",
    wazuh_rule: "#d29b54",
    mitre_technique: "#a788c6",
    cti_object: "#d87676",
    platform: "#4b809e",
    integration: "#65aaa1",
    metric: "#c7aa59",
    score: "#f0cf6b",
    reason_code: "#bd6c56",
    undeclared_endpoint: "#e4574f"
  };

  function option(select, value, label) {
    const element = document.createElement("option");
    element.value = value;
    element.textContent = label;
    select.appendChild(element);
  }

  function normalizedElements(raw) {
    const sourceElements = raw.elements || raw;
    const nodes = Array.isArray(sourceElements)
      ? sourceElements.filter((element) => !element.data?.source)
      : [...(sourceElements.nodes || [])];
    const edges = Array.isArray(sourceElements)
      ? sourceElements.filter((element) => element.data?.source)
      : [...(sourceElements.edges || [])];
    const declared = new Set(nodes.map((node) => String(node.data.id)));
    const placeholders = new Map();

    edges.forEach((edge) => {
      [edge.data.source, edge.data.target].forEach((endpoint) => {
        const id = String(endpoint);
        if (declared.has(id) || placeholders.has(id)) return;
        placeholders.set(id, {
          data: {
            id,
            label: id.replace(/^[^:]+:/, ""),
            type: "undeclared_endpoint",
            integrity_note: "Referenced by an edge but absent from saci_nodes_v2.csv"
          },
          classes: "integrity-warning"
        });
      });
      edge.classes = Number(edge.data.observed) === 1 ? "observed" : "missing";
    });
    return { nodes: nodes.concat([...placeholders.values()]), edges, declaredCount: nodes.length, placeholderCount: placeholders.size };
  }

  function detailPanel(node) {
    const panel = document.querySelector("[data-node-detail]");
    if (!panel) return;
    if (!node) {
      panel.innerHTML = '<p data-tr="Ayrıntıları görmek için bir düğüm seçin." data-en="Select a node to inspect its attributes.">Ayrıntıları görmek için bir düğüm seçin.</p>';
      window.dispatchEvent(new CustomEvent("saci:language", { detail: { lang: localStorage.getItem("saci-academic-language") || "tr" } }));
      return;
    }
    const data = node.data();
    panel.replaceChildren();
    const heading = document.createElement("h3");
    heading.textContent = data.label || data.id;
    panel.appendChild(heading);
    const list = document.createElement("dl");
    Object.entries(data)
      .filter(([, value]) => value !== "" && value !== null && value !== undefined)
      .forEach(([key, value]) => {
        const row = document.createElement("div");
        const term = document.createElement("dt");
        const description = document.createElement("dd");
        term.textContent = key;
        description.textContent = typeof value === "object" ? JSON.stringify(value) : String(value);
        row.append(term, description);
        list.appendChild(row);
      });
    panel.appendChild(list);
  }

  async function initGraph() {
    const container = document.getElementById("cy");
    if (!container || typeof cytoscape !== "function") return;
    const path = container.dataset.graphSource;
    const status = document.querySelector("[data-graph-status]");
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error(`${response.status} ${path}`);
      const raw = await response.json();
      const graph = normalizedElements(raw);

      const cy = cytoscape({
        container,
        elements: [...graph.nodes, ...graph.edges],
        wheelSensitivity: .25,
        minZoom: .18,
        maxZoom: 2.6,
        style: [
          { selector: "node", style: {
            "background-color": (element) => palette[element.data("type")] || "#7890a2",
            "border-color": "rgba(255,255,255,.55)",
            "border-width": 1,
            "label": "data(label)",
            "color": "#d9e6ed",
            "font-family": "Inter, Segoe UI, sans-serif",
            "font-size": 7,
            "text-wrap": "ellipsis",
            "text-max-width": 76,
            "text-valign": "bottom",
            "text-margin-y": 7,
            "width": 27,
            "height": 27,
            "overlay-opacity": 0
          }},
          { selector: 'node[type = "asset"]', style: { "width": 42, "height": 42, "font-size": 9, "font-weight": 700 } },
          { selector: 'node[type = "metric"], node[type = "score"]', style: { "shape": "round-rectangle", "width": 44, "height": 28 } },
          { selector: 'node[type = "undeclared_endpoint"]', style: {
            "shape": "diamond",
            "width": 38,
            "height": 38,
            "border-width": 3,
            "border-color": "#ffb0a9",
            "font-size": 8
          }},
          { selector: "edge", style: {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#688296",
            "line-color": "#688296",
            "width": 1,
            "opacity": .58,
            "arrow-scale": .55,
            "overlay-opacity": 0
          }},
          { selector: "edge.missing", style: { "line-color": "#e4574f", "target-arrow-color": "#e4574f", "line-style": "dashed", "width": 2.5 } },
          { selector: ":selected", style: { "border-color": "#fff", "border-width": 3, "opacity": 1 } },
          { selector: ".faded", style: { "opacity": .07 } },
          { selector: ".hidden", style: { "display": "none" } }
        ],
        layout: {
          name: "cose",
          animate: false,
          fit: true,
          padding: 40,
          nodeRepulsion: 7500,
          idealEdgeLength: 70,
          edgeElasticity: 90,
          gravity: .24,
          numIter: 900,
          randomize: true
        }
      });

      const typeSelect = document.querySelector('[data-graph-filter="type"]');
      const relationSelect = document.querySelector('[data-graph-filter="relationship"]');
      const search = document.querySelector('[data-graph-filter="search"]');
      const reset = document.querySelector("[data-graph-reset]");

      [...new Set(cy.nodes().map((node) => node.data("type")))].sort().forEach((type) => option(typeSelect, type, type.replaceAll("_", " ")));
      [...new Set(cy.edges().map((edge) => edge.data("relationship")))].sort().forEach((relation) => option(relationSelect, relation, relation));

      function applyFilters() {
        const type = typeSelect.value;
        const relation = relationSelect.value;
        const query = search.value.trim().toLowerCase();
        const nodes = cy.nodes();
        const edges = cy.edges();
        cy.elements().removeClass("faded hidden");

        let focusNodes = nodes;
        if (type !== "all") focusNodes = focusNodes.filter((node) => node.data("type") === type);
        if (query) focusNodes = focusNodes.filter((node) => JSON.stringify(node.data()).toLowerCase().includes(query));
        let focusEdges = relation === "all" ? edges : edges.filter((edge) => edge.data("relationship") === relation);

        if (type !== "all" || query) {
          const neighborhood = focusNodes.closedNeighborhood();
          cy.elements().difference(neighborhood).addClass("faded");
          focusEdges = focusEdges.intersection(neighborhood.edges());
        }
        if (relation !== "all") {
          edges.difference(focusEdges).addClass("faded");
          nodes.difference(focusEdges.connectedNodes()).addClass("faded");
        }

        const activeNodes = nodes.not(".faded");
        const activeEdges = edges.not(".faded");
        if (status) status.textContent = `${activeNodes.length} nodes · ${activeEdges.length} edges · ${graph.placeholderCount} integrity placeholders`;
      }

      typeSelect.addEventListener("change", applyFilters);
      relationSelect.addEventListener("change", applyFilters);
      search.addEventListener("input", applyFilters);
      reset.addEventListener("click", () => {
        typeSelect.value = "all";
        relationSelect.value = "all";
        search.value = "";
        cy.elements().removeClass("faded hidden");
        cy.fit(undefined, 35);
        applyFilters();
      });
      cy.on("tap", "node", (event) => detailPanel(event.target));
      cy.on("tap", (event) => { if (event.target === cy) detailPanel(null); });
      applyFilters();
    } catch (error) {
      console.error("SACI graph could not be loaded", error);
      if (status) status.textContent = "Graph data could not be loaded. Use the accessible tables below.";
    }
  }

  document.addEventListener("DOMContentLoaded", initGraph);
})();
