import os

# Create main folder and assets folder
base = "luxury_site"
os.makedirs(base, exist_ok=True)
os.makedirs(os.path.join(base, "assets"), exist_ok=True)

# ------------- Helper Function -------------
def write_file(name, content):
    path = os.path.join(base, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created {name}")

# ------------- CSS File -------------
styles_css = """
/* styles.css - базовые стили */
* { box-sizing: border-box; }
body {
  font-family: Arial, Helvetica, sans-serif;
  margin: 0;
  background: #fafafa;
  color: #222;
}
.container { max-width: 1000px; margin: 20px auto; padding: 0 16px; }
header { background: #111; color: #fff; padding: 16px; }
header h1 { margin: 0; font-size: 20px; }
nav { margin-top: 8px; }
nav a { color: #fff; margin-right: 12px; text-decoration: none; font-size: 14px; }
.hero { background: linear-gradient(90deg,#222,#444); color: #fff; padding: 30px; border-radius: 8px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 16px; margin-top: 16px; }
.card { background: #fff; padding: 12px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
.product-img { height: 160px; background: #eee; display:flex; align-items:center; justify-content:center; color:#666; border-radius:6px; font-size:14px; }
.footer { padding: 20px; text-align: center; color: #666; margin-top: 30px; }
.button { background: #111; color: white; padding: 8px 12px; border-radius: 6px; text-decoration: none; display: inline-block; }
.small { font-size: 13px; color: #666; }
h2,h3 { margin-top: 0; }
@media (max-width:600px){
  header h1 { font-size: 16px; }
  .product-img { height: 120px; }
}
"""
write_file("styles.css", styles_css)

# ------------- JavaScript File -------------
script_js = """
// script.js - логика каталога и корзины (localStorage)
const PRODUCTS = [
  {id:1, brand:'Chanel', model:'Classic Flap', price:4200},
  {id:2, brand:'Gucci', model:'Dionysus', price:4300},
  {id:3, brand:'Louis Vuitton', model:'Neverfull', price:2500},
  {id:4, brand:'Prada', model:'Galleria', price:3100}
];

function renderCatalog(){
  const grid = document.getElementById('catalog');
  if(!grid) return;
  PRODUCTS.forEach(p=>{
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
      <div class="product-img">${p.brand} ${p.model}</div>
      <h3>${p.brand} ${p.model}</h3>
      <p class="small">Цена: €${p.price.toLocaleString()}</p>
      <a class="button" href="#" onclick="addToCart(${p.id});return false;">В корзину</a>
      <a class="small" href="product.html?id=${p.id}" style="margin-left:8px">Подробнее</a>
    `;
    grid.appendChild(div);
  });
}

function addToCart(id){
  const cart = JSON.parse(localStorage.getItem('cart')||'[]');
  cart.push(id);
  localStorage.setItem('cart', JSON.stringify(cart));
  alert('Добавлено в корзину');
  updateCartCount();
}

function updateCartCount(){
  const el = document.getElementById('cart-count');
  if(!el) return;
  const c = JSON.parse(localStorage.getItem('cart')||'[]').length;
  el.innerText = c;
}

function renderCart(){
  const list = document.getElementById('cart-list');
  if(!list) return;
  list.innerHTML = '';
  const cart = JSON.parse(localStorage.getItem('cart')||'[]');
  if(cart.length===0){ list.innerHTML = '<p>Корзина пуста</p>'; return; }
  let sum = 0;
  cart.forEach((id, idx)=>{
    const p = PRODUCTS.find(x=>x.id===id);
    sum += p.price;
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `<h4>${p.brand} ${p.model}</h4><p class="small">€${p.price}</p>
      <a class="button" href="#" onclick="removeFromCart(${idx});return false;">Удалить</a>`;
    list.appendChild(div);
  });
  const total = document.createElement('div');
  total.className = 'card';
  total.innerHTML = `<h3>Итого: €${sum.toLocaleString()}</h3>`;
  list.appendChild(total);
}

function removeFromCart(idx){
  const cart = JSON.parse(localStorage.getItem('cart')||'[]');
  cart.splice(idx,1);
  localStorage.setItem('cart', JSON.stringify(cart));
  renderCart();
  updateCartCount();
}

function renderProductPage(){
  const el = document.getElementById('product');
  if(!el) return;
  const params = new URLSearchParams(location.search);
  const id = Number(params.get('id') || 0);
  const p = PRODUCTS.find(x=>x.id===id);
  if(!p){ el.innerHTML = '<p>Товар не найден</p>'; return; }
  el.innerHTML = `
    <div class="card">
      <div class="product-img">${p.brand} ${p.model}</div>
      <h2>${p.brand} ${p.model}</h2>
      <p class="small">Цена: €${p.price.toLocaleString()}</p>
      <p class="small">Сертификат подлинности включён. Ограниченная серия.</p>
      <a class="button" href="#" onclick="addToCart(${p.id});return false;">Добавить в корзину</a>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', ()=>{
  updateCartCount();
  if(document.getElementById('catalog')) renderCatalog();
  if(document.getElementById('cart-list')) renderCart();
  if(document.getElementById('product')) renderProductPage();
});
"""
write_file("script.js", script_js)

# ------------- HTML Pages -------------
pages = {
    "index.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Luxury Bags — Главная</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>Luxury Bags — Онлайн-магазин</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='cart.html'>Корзина (<span id='cart-count'>0</span>)</a> <a href='about.html'>О проекте</a> <a href='marketing.html'>План</a></nav></header><main class='container'><section class='hero'><h2>Премиальные женские сумки — гарантированная подлинность</h2><p>Эксклюзивные коллекции и VIP-сервис. Просмотрите каталог и получите персональную консультацию.</p><a class='button' href='catalog.html'>Перейти в каталог</a></section></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer><script src='script.js'></script></body></html>""",
    "catalog.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Каталог</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>Каталог</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='cart.html'>Корзина (<span id='cart-count'>0</span>)</a> <a href='about.html'>О проекте</a> <a href='marketing.html'>План</a></nav></header><main class='container'><div id='catalog' class='grid'></div></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer><script src='script.js'></script></body></html>""",
    "product.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Товар</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>Информация о товаре</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='cart.html'>Корзина (<span id='cart-count'>0</span>)</a> <a href='about.html'>О проекте</a> <a href='marketing.html'>План</a></nav></header><main class='container'><div id='product'></div></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer><script src='script.js'></script></body></html>""",
    "cart.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Корзина</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>Корзина</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='cart.html'>Корзина (<span id='cart-count'>0</span>)</a> <a href='about.html'>О проекте</a> <a href='marketing.html'>План</a></nav></header><main class='container'><div id='cart-list'></div></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer><script src='script.js'></script></body></html>""",
    "about.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>О проекте</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>О проекте</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='cart.html'>Корзина (<span id='cart-count'>0</span>)</a> <a href='about.html'>О проекте</a> <a href='marketing.html'>План</a></nav></header><main class='container'><h2>Проект: Продажа женских luxury сумок</h2><p class='small'>Этот демонстрационный сайт использует данные из вашего маркетингового плана и диаграмм.</p></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer><script src='script.js'></script></body></html>""",
    "marketing.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Маркетинговый план</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>Маркетинговый план и диаграммы</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='cart.html'>Корзина (<span id='cart-count'>0</span>)</a> <a href='about.html'>О проекте</a> <a href='marketing.html'>План</a></nav></header><main class='container'><h2>Документы</h2><div class='grid'><div class='card'><h4>Маркетинговый план</h4><a class='button' href='assets/marketing_plan.pdf' target='_blank'>Открыть PDF</a></div><div class='card'><h4>Диаграммы</h4><a class='button' href='assets/diagram.pdf' target='_blank'>Открыть PDF</a></div><div class='card'><h4>Тема ИС</h4><a class='button' href='assets/tema_IS.pdf' target='_blank'>Открыть PDF</a></div></div></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer><script src='script.js'></script></body></html>""",
    "admin.html": """<!doctype html><html lang='ru'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Админ</title><link rel='stylesheet' href='styles.css'></head><body><header class='container'><h1>Админ-панель (заглушка)</h1><nav><a href='index.html'>Главная</a> <a href='catalog.html'>Каталог</a> <a href='admin.html'>Админ</a></nav></header><main class='container'><div class='card'><h3>Функции (в будущем)</h3><ul><li>Управление товарами</li><li>Просмотр заказов</li><li>CRM</li></ul></div></main><footer class='footer'>© Luxury Bags — Демонстрационный сайт</footer></body></html>"""
}

for name, html in pages.items():
    write_file(name, html)

print("\n✅ Website created in folder:", os.path.abspath(base))
print("You can open 'index.html' in your browser.")
