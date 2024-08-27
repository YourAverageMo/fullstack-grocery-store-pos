document.addEventListener("DOMContentLoaded", function () {
    fetch('/getproducts')
        .then(response => response.json())
        .then(data => {
            const productsDiv = document.getElementById('products');
            if (data.length > 0) {
                let html = '<ul class="list-group">';
                data.forEach(product => {
                    html += `<li class="list-group-item">${product.name} - ${product.price}</li>`;
                });
                html += '</ul>';
                productsDiv.innerHTML = html;
            } else {
                productsDiv.innerHTML = '<p>No products available.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            document.getElementById('products').innerHTML = '<p>Error loading products.</p>';
        });
});
