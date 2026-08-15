// $('.add-cart').click(function(e){
//     e.preventDefault();

//     var service_id = $(this).closest('.service_data').find('.service_id').val();
//     var token = $('input[name=csrfmiddlewaretoken]').val();
//     console.log("Button clicked");
//     console.log(service_id);
//     $.ajax({
//         method: 'POST',
//         url: '/add-cart/',
//         data: {
//             'service_id': service_id,
//             csrfmiddlewaretoken: token
//         },
//         success: function (response) {
//             console.log(response)
//             alertify.success(response.status)
//         }
//     })
// })

// const btn = document.getElementById('hello-btn')

// btn.addEventListener('click', function(){
//     fetch('/test-fetch/')
//     .then(response => response.json())
//     .then(data=>{
//         alert(data.message);
//     });
// });



const miniCartContainer = document.querySelector('#mini-cart-container');
const cartContainer = document.querySelector('#cart-container');
const cartPageItems = cartContainer ? cartContainer.querySelectorAll('.cart-item') : [];
const cartAddBtns = document.querySelectorAll('.add-cart');
const cartDelBtns = document.querySelectorAll('.del-cart');
const incBtns = document.querySelectorAll('.inc-btn');
const decBtns = document.querySelectorAll('.dec-btn');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
const cartCount = document.querySelector('#cart-count')


cartPageItems.forEach( item => {
    updateDecBtn(item)
});

cartAddBtns.forEach( btn => {
    btn.addEventListener('click', function(){
        const serviceId = this.dataset.id;
        fetch('/add-cart/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                service_id: serviceId
            })
        })
        .then(response=> response.json())
        .then(data=>{
            alertify.success(data.status)
            cartCount.classList.remove('d-none')
            cartCount.textContent = data.cart_count;
            addMiniCartItem(data)
            updateSummary(data)
        });
    });
});

// miniCartContainer.addEventListener('click', function(e){
//     const btn =  e.target.closest('.del-cart');
//     const cartId = this.dataset.id;
    
//     const mainCartItem = cartContainer ? cartContainer.querySelector(
//         `.cart-item[data-id="${cartId}"]`
//     ) : null;
//     const miniCartItem = miniCartContainer.querySelector(
//         `.cart-item[data-id="${cartId}"]`
//     );
//     if (!btn) return;

//     fetch('/del-cart/',{
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken
//         },
//         body: JSON.stringify({
//             cart_id: cartId
//         })
//     })
//     .then(response=> response.json())
//     .then(data=>{

//         if (data.status === 'Cart removed'){


//             if(mainCartItem){
//                 mainCartItem.remove();
//             }
//             miniCartItem.remove();
//             cartCount.textContent = data.cart_count;
//             updateSummary(data);

//             if (data.cart_count === 0){
                
//                 cartCount.textContent = '';
//                 cartCount.classList.add('d-none');
                
//                 cartContainer.innerHTML = `
//                     <div class="py-5">
//                         <h3 class="text-center py-5">
//                             Your cart is empty
//                         </h3>
//                     </div>
//                 `;
//                 miniCartContainer.innerHTML = `
//                     <div class="text-center py-3" id='empty-cart'>
//                         Your cart is empty
//                     </div>
//                 `;
//             }

//             alertify.success(data.status);
//         }

//     });

// })

miniCartContainer.addEventListener('click', function(event){
    const btn = event.target.closest('.del-cart');
    if (!btn) return;
    deleteCartItem(btn.dataset.id);
})

if (cartContainer) {
    cartContainer.addEventListener('click', function(event){
        const btn = event.target.closest('.del-cart');
        if (!btn) return;
        deleteCartItem(btn.dataset.id);
    });
}

function deleteCartItem(cartId){
    const miniCartContainer = document.querySelector('#mini-cart-container');
    const cartContainer = document.querySelector('#cart-container'); 
    const mainCartItem = cartContainer ? cartContainer.querySelector(
        `.cart-item[data-id="${cartId}"]`
    ) : null;
    const miniCartItem = miniCartContainer.querySelector(
        `.cart-item[data-id="${cartId}"]`
    );
    console.log(miniCartItem);
    
    

    fetch('/del-cart/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            cart_id: cartId
        })
    })
    .then(response=> response.json())
    .then(data=>{

        if (data.status === 'Cart removed'){


            if(mainCartItem){
                mainCartItem.remove();
            }
            if(miniCartItem){
                miniCartItem.remove();
            }
            cartCount.textContent = data.cart_count;
            updateSummary(data);

            if (data.cart_count === 0){
                
                cartCount.textContent = '';
                cartCount.classList.add('d-none');
                
                if (cartContainer){
                    cartContainer.innerHTML = `
                        <div class="py-5">
                            <h3 class="text-center py-5">
                                Your cart is empty
                            </h3>
                        </div>
                    `;
                }
                if (miniCartContainer){

                    miniCartContainer.innerHTML = `
                        <div class="text-center py-3" id='empty-cart'>
                            Your cart is empty
                        </div>
                    `;
                }
            }
            alertify.success(data.status);
        }
    });
}


function updateDecBtn(row) {
    const qty = parseInt(
        row.querySelector('.service-qty').value
    );
    const decBtn = row.querySelector('.dec-btn');

    decBtn.disabled = qty <= 1;
};



function updateSummary(data){
    
    const subtotal = document.querySelector('.subtotal');
    const gst = document.querySelector('.gst');
    const total = document.querySelector('.total')

    if (!subtotal || !gst || !total) {
        return;
    }

    subtotal.textContent = '₹'+ parseFloat(data.subtotal).toFixed(2)
    gst.textContent = '₹'+ parseFloat(data.gst).toFixed(2)
    total.textContent = '₹'+ parseFloat(data.total).toFixed(2)

};

function addMiniCartItem(data){

    const item = document.createElement('div');

    item.classList.add(
        'cart-item',
        'd-flex',
        'justify-content-between',
        'align-items-center',
        'gap-2'
    );
    item.dataset.id = data.cart_id;

    item.innerHTML = `
        <a href="${data.service_url}" class="nav-link d-flex align-items-center gap-2">
            <div class="d-flex justify-content-center align-items-center overflow-hidden rounded" style="width: 25px; height: 25px;">
                <img src="${data.service_image}" alt="service image" class="d-block h-100">
            </div>
            <span class="d-flex flex-column">
                <span class="fw-bold">
                    ${data.service_name}
                </span>
                <span class="" style="font-size: 12px;">
                    Duration: ${data.service_duration}
                    ${data.is_under_hour
                        ?`<span class="text-success">
                            <i class="bi bi-lightning-fill"></i>
                            </span>`
                        : ''
                    }
                </span>
            </span>
        </a>
        <button class="btn btn-close pe-3 del-cart" data-id="${data.cart_id}"></button>`;
    
    if(data.cart_count === 1 ){
        const emptyCart = miniCartContainer.querySelector('#empty-cart')
        if (emptyCart){

            emptyCart.remove()
        }
    };
    miniCartContainer.appendChild(item);
};

incBtns.forEach(
    
    btn => {
        
        btn.addEventListener('click', function(){
            
            
            
            const row = this.closest('.cart-item');
            const cartId = row.dataset.id;
            
            const qtyInput = row.querySelector('.service-qty');
            
            const servicePrice = row.querySelector('.service-price');
            const totalPrice = row.querySelector('.total-price');
            const price = parseFloat(servicePrice.dataset.price);
            
            let qty = parseInt(qtyInput.value);
            qty++;
            qtyInput.value = qty;
            updateDecBtn(row)
            let total = price * qty;
            totalPrice.textContent = '₹'+total.toFixed(2);

            fetch('/update-cart/',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    cart_id: cartId,
                    qty: qty
                })
            })
            .then(response=> response.json())
            .then(data=>{
                alertify.success(data.status)
                updateSummary(data)

            });


        });
    }
);

decBtns.forEach(
    btn => {
        btn.addEventListener('click', function(){
            
            const row = this.closest('.cart-item');
            const cartId = row.dataset.id;

            const decBtn = row.querySelector('.dec-btn');

            const qtyInput = row.querySelector('.service-qty');

            
            
            const servicePrice = row.querySelector('.service-price');
            const totalPrice = row.querySelector('.total-price');
            const price = parseFloat(servicePrice.dataset.price);
            
            
            let qty = parseInt(qtyInput.value);

            if (qty > 1) {
                qty--;
                qtyInput.value = qty;
                updateDecBtn(row)
                let total = price * qty;

                totalPrice.textContent = '₹'+total.toFixed(2);

                fetch('/update-cart/',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        cart_id: cartId,
                        qty: qty
                    })
                })
                .then(response=> response.json())
                .then(data=>{
                    alertify.success(data.status)
                    updateSummary(data)
                });
            };


        });
    }
);