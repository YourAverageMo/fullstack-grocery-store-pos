document.addEventListener("DOMContentLoaded", function () {
    const refreshButton = document.querySelector('.btn-primary');
    const tableBody = document.querySelector('table tbody');

    function fetchProducts() {
        fetch('/getproducts')
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    let html = '';
                    data.forEach(product => {
                        html += `
                            <tr data-id="${product[0]}">
                                <td>${product[0]}</td>
                                <td>${product[1]}</td>
                                <td>${product[2]}</td>
                                <td>${product[3]}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm me-2 delete-btn">Delete</button>
                                    <button class="btn btn-primary btn-sm">Edit</button>
                                </td>
                            </tr>
                        `;
                    });
                    tableBody.innerHTML = html;
                } else {
                    tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No products available.</td></tr>';
                }
            })
            .catch(error => {
                console.error('Error fetching products:', error);
                tableBody.innerHTML = '<tr><td colspan="5" class="text-center">Error loading products.</td></tr>';
            });
    }

    function deleteProduct(productId) {
        fetch('/deleteproduct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_ids: [productId] })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    fetchProducts(); // Refresh the table after deletion
                } else {
                    alert('Error deleting product: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error deleting product:', error);
                alert('Error deleting product.');
            });
    }

    // Fetch products on page load
    fetchProducts();

    // Add event listener to the refresh button
    refreshButton.addEventListener('click', fetchProducts);

    // Event delegation for delete buttons
    tableBody.addEventListener('click', function (event) {
        if (event.target.classList.contains('delete-btn')) {
            const row = event.target.closest('tr');
            const productId = row.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this product?')) {
                deleteProduct(productId);
            }
        }
    });
});
