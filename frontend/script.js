const API_BASE = "https://recipes-awbz.onrender.com/api/recipes";

let page = 1;
let limit = 15;

async function loadRecipes() {
  const res = await fetch(`${API_BASE}?page=${page}&limit=${limit}`);
  const data = await res.json();

  document.getElementById("pageInfo").innerText =
    `Page ${data.page} of ${Math.ceil(data.total / limit)}`;

  renderTable(data.data);
}

function renderTable(recipes) {
  const tbody = document.getElementById("recipesTable");
  tbody.innerHTML = "";

  recipes.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${r.title}</td>
      <td>${r.cuisine}</td>
      <td>⭐ ${r.rating ?? "-"}</td>
      <td>${r.total_time ?? "-"}</td>
      <td>${r.serves ?? "-"}</td>
    `;
    tr.onclick = () => openDrawer(r);
    tbody.appendChild(tr);
  });
}

function renderNutrition(nutrients) {
  if (!nutrients) return "<p>No nutrition data available</p>";

  const labelMap = {
    calories: "Calories",
    fatContent: "Fat",
    fiberContent: "Fiber",
    sugarContent: "Sugar",
    sodiumContent: "Sodium",
    proteinContent: "Protein",
    cholesterolContent: "Cholesterol",
    carbohydrateContent: "Carbohydrates",
    saturatedFatContent: "Saturated Fat",
    unsaturatedFatContent: "Unsaturated Fat"
  };

  return `
    <ul class="nutrition-list">
      ${Object.entries(labelMap)
        .filter(([key]) => nutrients[key])
        .map(
          ([key, label]) =>
            `<li><strong>${label}:</strong> ${nutrients[key]}</li>`
        )
        .join("")}
    </ul>
  `;
}

function openDrawer(recipe) {
  const drawer = document.getElementById("drawer");
  drawer.classList.remove("hidden");

  const steps = recipe.instructions
    ? recipe.instructions.map((s, i) => `<li>${s}</li>`).join("")
    : "<li>No instructions available</li>";

  const nutritionHtml = renderNutrition(recipe.nutrients);

  document.getElementById("drawerContent").innerHTML = `
    <h2>${recipe.title}</h2>
    <p><strong>Cuisine:</strong> ${recipe.cuisine}</p>

    <p>${recipe.description ?? ""}</p>

    <h3>Instructions</h3>
    <ol>${steps}</ol>

    <h3>Nutrition</h3>
    ${nutritionHtml}
  `;
}



function closeDrawer() {
  document.getElementById("drawer").classList.add("hidden");
}

function nextPage() {
  page++;
  loadRecipes();
}

function prevPage() {
  if (page > 1) {
    page--;
    loadRecipes();
  }
}

async function searchRecipes() {
  const params = new URLSearchParams();

  const title = titleFilter.value;
  const cuisine = cuisineFilter.value;
  const rating = ratingFilter.value;
  const calories = caloriesFilter.value;

  if (title) params.append("title", title);
  if (cuisine) params.append("cuisine", cuisine);
  if (rating) params.append("rating", rating);
  if (calories) params.append("calories", calories);

  const res = await fetch(`${API_BASE}/search?${params}`);
  const data = await res.json();
  renderTable(data.data);
}

loadRecipes();
