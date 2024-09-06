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
                                    <button class="btn btn-primary btn-sm edit-btn">Edit</button>
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

    // Event delegation for edit buttons
    tableBody.addEventListener('click', function (event) {
        if (event.target.classList.contains('edit-btn')) {
            const row = event.target.closest('tr');
            const productId = row.getAttribute('data-id');

            // Get the current values of the product
            const currentName = row.querySelector('td:nth-child(2)').textContent;
            const currentUnits = row.querySelector('td:nth-child(3)').textContent;
            const currentPrice = row.querySelector('td:nth-child(4)').textContent;

            // Replace the table data cells with input fields for editing
            row.querySelector('td:nth-child(2)').innerHTML = `<input type="text" class="form-control edit-name" value="${currentName}">`;
            row.querySelector('td:nth-child(3)').innerHTML = `
            <select class="form-select edit-units">
                <option value="1" ${currentUnits == 1 ? 'selected' : ''}>1 (kg)</option>
                <option value="2" ${currentUnits == 2 ? 'selected' : ''}>2 (each)</option>
            </select>`;
            row.querySelector('td:nth-child(4)').innerHTML = `<input type="text" class="form-control edit-price" value="${currentPrice}">`;

            // Add Save and Cancel buttons
            const actionCell = row.querySelector('td:nth-child(5)');
            actionCell.innerHTML = `
                <button class="btn btn-success btn-sm me-2 save-btn">Save</button>
                <button class="btn btn-secondary btn-sm cancel-btn">Cancel</button>
            `;
        }
    });

    // Event delegation for Save button
    tableBody.addEventListener('click', function (event) {
        if (event.target.classList.contains('save-btn')) {
            const row = event.target.closest('tr');
            const productId = row.getAttribute('data-id');
            const newName = row.querySelector('.edit-name').value;
            const newUnits = row.querySelector('.edit-units').value;
            const newPrice = row.querySelector('.edit-price').value;

            // Send data to the server via a PUT/POST request
            fetch(`/editproduct/${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: newName,
                    units: newUnits,
                    price: newPrice
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the row with the new values
                        row.innerHTML = `
                    <td>${productId}</td>
                    <td>${newName}</td>
                    <td>${newUnits}</td>
                    <td>${newPrice}</td>
                    <td>
                        <button class="btn btn-danger btn-sm me-2 delete-btn">Delete</button>
                        <button class="btn btn-primary btn-sm edit-btn">Edit</button>
                    </td>
                `;
                    } else {
                        alert('Error updating product.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error updating product.');
                });
        }
    });

    // Cancel button just refreshes products
    tableBody.addEventListener('click', function (event) {
        if (event.target.classList.contains('cancel-btn')) { fetchProducts(); }
    });

    // Insert product event listener
    document.querySelector('#insertProductRow .btn-success').addEventListener('click', function () {
        const productName = document.getElementById('newProductName').value;
        const productUnits = parseInt(document.getElementById('newProductUnits').value);
        const productPrice = parseFloat(document.getElementById('newProductPrice').value);

        if (productName && !isNaN(productUnits) && !isNaN(productPrice)) {
            // Create a new product object
            const newProduct = {
                name: productName,
                units: productUnits,
                price: productPrice
            };

            // Send the new product to the server
            fetch('/insertproduct', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newProduct)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // refresh the product list after insertion
                        window.location.reload();
                    } else {
                        console.error('Error inserting product:', data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            alert("Please enter valid product details.");
        }
    });

});
