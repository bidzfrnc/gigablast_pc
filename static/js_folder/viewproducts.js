document.addEventListener("click", function(event) {
    // ... Your existing event listeners ...

    // "Cancel" button is clicked
    if (event.target.id === "CancelBtn") {
        var orderForm = event.target.closest(".popupOrderForm");
        var form = orderForm.querySelector("form");
        
        // Reset the form
        form.reset();

        // Reset the total price to the initial value (assuming the initial value is stored as a data attribute)
        var totalPriceElement = orderForm.querySelector(".total_price");
        var initialPrice = parseFloat(totalPriceElement.getAttribute("data-product-price"));
        totalPriceElement.textContent = "₱ " + initialPrice.toFixed(2);
        
        // Remove the "active" class to hide the order form
        orderForm.classList.remove("active");
    }

document.addEventListener("click", function(event) {
    // ... Your existing event listeners ...

    // "Cancel" button is clicked
    if (event.target.id === "CancelBtn") {
        var orderForm = event.target.closest(".popupOrderForm");
        var form = orderForm.querySelector("form");
        
        // Reset the form
        form.reset();
        
        // Remove the "active" class to hide the order form
        orderForm.classList.remove("active");
    }

document.addEventListener("click", function(event) {
    // "View Specification" button is clicked
    if (event.target.classList.contains("btn_spec")) {
        // Close currently open specifications
        closeAllSpecifications();

        var specs = event.target.nextElementSibling;
        specs.classList.add("active");

        // Close any open "btn_buy" popups
        closeAllOrderForms();
    }

    // "Close" button inside a specification popup is clicked
    if (event.target.id === "closeSpecButton") {
        var specs = event.target.closest(".popupSpecs");
        specs.classList.remove("active");
    }

    // "Buy Now" button is clicked
    if (event.target.classList.contains("btn_buy")) {
        // Close currently open order forms
        closeAllOrderForms();

        var orderForm = event.target.nextElementSibling;
        orderForm.classList.add("active");

        // Close any open "btn_spec" popups
        closeAllSpecifications();
    }

    // "Close" button inside an order form popup is clicked
    if (event.target.id === "CancelBtn") {
        var orderForm = event.target.closest(".popupOrderForm");
        orderForm.classList.remove("active");
    }

    // Check if a .popupSpecs element is clicked
    if (event.target.classList.contains("popupSpecs")) {
        // Close currently open order forms
        closeAllOrderForms();
    }


    
});

function closeAllSpecifications() {
    var openSpecs = document.querySelectorAll(".popupSpecs.active");
    openSpecs.forEach(function(specs) {
        specs.classList.remove("active");
    });
}

function closeAllOrderForms() {
    var openOrderForms = document.querySelectorAll(".popupOrderForm.active");
    openOrderForms.forEach(function(orderForm) {
        orderForm.classList.remove("active");
    });
}


});

document.addEventListener("input", function(event) {
    // Check if the event is triggered by a quantity input field
    if (event.target.classList.contains("quantity_field")) {
        // Get the quantity input element and the corresponding total price element
        var quantityInput = event.target;
        var totalPriceElement = quantityInput.closest(".quantity_price").querySelector(".total_price");
        
        // Get the product price and quantity values
        var productPrice = parseFloat(totalPriceElement.getAttribute("data-product-price"));
        var quantity = parseInt(quantityInput.value);
        
        // Calculate the new total price
        var newTotalPrice = productPrice * quantity;
        
        // Update the total price element with the new value
        totalPriceElement.textContent = "₱ " + newTotalPrice.toFixed(2);
        }
    });
});