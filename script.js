// =====================================================
// Guia Gastronômico Casa Terras Altas
// script.js - MVP V1
// =====================================================

let restaurantes = [];
let restaurantesFiltrados = [];

//======================================================
// CARREGAR JSON
//======================================================

async function carregarRestaurantes() {

    try {

        const resposta = await fetch("restaurantes.json");

        restaurantes = await resposta.json();

        restaurantesFiltrados = [...restaurantes];

        renderizar(restaurantesFiltrados);

    } catch (erro) {

        console.error("Erro ao carregar restaurantes:", erro);

        document.getElementById("restaurantGrid").innerHTML = `
            <p style="text-align:center;padding:40px;">
                Não foi possível carregar os restaurantes.
            </p>
        `;

    }

}

//======================================================
// RENDERIZAR CARDS
//======================================================

function renderizar(lista) {

    const grid = document.getElementById("restaurantGrid");

    grid.innerHTML = "";

    if (lista.length === 0) {

        grid.innerHTML = `
            <p style="text-align:center;padding:40px;">
                Nenhum restaurante encontrado.
            </p>
        `;

        return;

    }

    lista.forEach(restaurante => {

        const card = document.createElement("article");

        card.className = "restaurant-card";

        const link = restaurante.site || restaurante.instagram || restaurante.maps || '#';

        // Origem fixa: Casa Terras Altas
        const origem = 'Rua K, 225, Campos do Jordão';

        // Montar destino amigável: nome + bairro (se disponível)
        const destinoText = `${restaurante.nome} ${restaurante.bairro || ''} Campos do Jordão`;

        const directionsUrl = `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(origem)}&destination=${encodeURIComponent(destinoText)}`;

        // montar link de visita (site > instagram > maps)
        const visitLink = restaurante.site || restaurante.instagram || restaurante.maps || null;

        const visitButtonHtml = visitLink
            ? `<a href="${visitLink}" target="_blank" rel="noopener noreferrer" class="visit-button">Visitar</a>`
            : `<button class="visit-button disabled" disabled>Visitar</button>`;

        card.innerHTML = `

            <div class="restaurant-content no-image">

                <h3>${restaurante.nome}</h3>

                <p>

                    ⭐ ${restaurante.nota} • ${restaurante.categoria} ${restaurante.preco ? '• ' + restaurante.preco : ''}

                </p>

                ${restaurante.valor_medio ? `<p class="price-info">💰 ${restaurante.valor_medio}</p>` : ''}

                <p>

                    ${restaurante.descricao}

                </p>

                ${restaurante.endereco ? `<p class="endereco-info">📍 ${restaurante.endereco}</p>` : ''}

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

//======================================================
// PESQUISA
//======================================================

function pesquisar(texto) {

    texto = texto.toLowerCase();

    restaurantesFiltrados = restaurantes.filter(r =>

        r.nome.toLowerCase().includes(texto)

        ||

        r.categoria.toLowerCase().includes(texto)

        ||

        r.bairro.toLowerCase().includes(texto)

    );

    renderizar(restaurantesFiltrados);

}

//======================================================
// FILTRO POR TAGS / EXPERIÊNCIA
//======================================================

function filtrarPorExperiencia(tag) {

    if (tag === "Todos") {

        restaurantesFiltrados = [...restaurantes];

    } else {

        restaurantesFiltrados = restaurantes.filter(r =>

            (r.tags && r.tags.some(t => t.toLowerCase() === tag.toLowerCase())) || 
            (r.categoria && r.categoria.toLowerCase() === tag.toLowerCase())

        );

    }

    renderizar(restaurantesFiltrados);

}

//======================================================
// EVENTOS
//======================================================

document.addEventListener("DOMContentLoaded", () => {

    carregarRestaurantes();

    const pesquisa = document.getElementById("searchInput");

    pesquisa.addEventListener("keyup", e => {

        pesquisar(e.target.value);

    });

    document.querySelectorAll(".categories button")

        .forEach(botao => {

            botao.addEventListener("click", () => {
                
                document.querySelectorAll(".categories button").forEach(b => b.classList.remove("active"));
                botao.classList.add("active");
                
                const tag = botao.innerText.trim();
                filtrarPorExperiencia(tag === "Todos" ? "Todos" : tag.toLowerCase());
            });

        });
                document.querySelectorAll(".categories button")
        .forEach(botao => {
            botao.addEventListener("click", () => {
                document.querySelectorAll(".categories button").forEach(b => b.classList.remove("active"));
                botao.classList.add("active");
                
                let categoria = botao.textContent
                    .replace(/[^\wÀ-ÿ ]/g, "")
                    .trim();
                filtrarPorExperiencia(categoria === "Todos" ? "Todos" : categoria);
            });
        });
});
