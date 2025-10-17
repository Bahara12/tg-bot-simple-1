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