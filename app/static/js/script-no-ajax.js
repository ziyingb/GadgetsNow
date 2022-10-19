var stripe = Stripe('pk_test_51LudtbH9RvLfX3o6FSoGYQxQisM9hz1chTbZl761XDY4HhHcaEWYpKtIXZmqjmm6zSTVuXQpISLh0Q8ZJTqDciby002Py4s5oS');

const button = document.querySelector('#buy_now_btn');
button.addEventListener('click', event =>{
    stripe.redirectToCheckout({
        sessionId: checkout_session_id
    }).then(function (result){

    });
});