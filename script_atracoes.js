// script_atracoes.js
// Script para gerenciar a exibição das atrações turísticas

let atracoes = [];
let atracoesFiltradas = [];

async function carregarAtracoes() {
    try {
        const resposta = await fetch("atracoes.json");
        atracoes = await resposta.json();
        atracoesFiltrados = [...atracoes];
        renderizar(atracoes);
    } catch (erro) {
        console.error("Erro ao carregar atrações:", erro);
    }
}

function renderizar(lista) {
    const grid = document.getElementById("attractionGrid");
    grid.innerHTML = "";

    if (lista.length === 0) {
        grid.innerHTML = '<p style="text-align:center;padding:40px;">Nenhuma atração encontrada.</p>';
        return;
    }

    lista.forEach(atracao => {
        const card = document.createElement("article");
        card.className = "restaurant-card";
        
        // Origem fixa: Casa Terras Altas
        const origem = 'Rua K, 225, Campos do Jordão';
        const directionsUrl = `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(origem)}&destination=${encodeURIComponent(atracao.nome + " Campos do Jordão")}`;

        const visitLink = atracao.maps || `https://www.google.com/search?q=${encodeURIComponent(atracao.nome + " Campos do Jordão")}`;
        const visitButtonHtml = `<a href="${visitLink}" target="_blank" rel="noopener noreferrer" class="visit-button">Visitar</a>`;

        card.innerHTML = `
            <div class="restaurant-content">
                <h3>${atracao.nome}</h3>
                <p>⭐ ${atracao.nota} • ${atracao.categoria}</p>
                ${atracao.valor_entrada ? `<p class="price-info">💰 ${atracao.valor_entrada}</p>` : ''}
                <p>${atracao.descricao}</p>
                <p>📍 ${atracao.endereco}</p>
                <br>
                <div class="card-actions">
                    ${visitButtonHtml}
                    <a href="${directionsUrl}" target="_blank" rel="noopener noreferrer" class="map-button">Como Chegar</a>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function filtrarPorExperiencia(tag) {
    const lista = (tag === "Todos") ? atracoes : atracoes.filter(a => a.tags.includes(tag.toLowerCase()));
    renderizar(lista);
}

document.addEventListener("DOMContentLoaded", () => {
    carregarAtracoes();
    
    // Configura botões de filtro
    document.querySelectorAll(".experience-grid button").forEach(botao => {
        botao.addEventListener("click", (e) => {
            document.querySelectorAll(".experience-grid button").forEach(b => b.classList.remove("active"));
            e.target.classList.add("active");
            
            const tag = e.target.innerText.toLowerCase().replace(/[^a-z]/g, "");
            filtrarPorExperiencia(tag === "todos" ? "Todos" : tag);
        });
    });
});