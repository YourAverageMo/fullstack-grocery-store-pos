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
                            <tr>
                                <td>${product[0]}</td>
                                <td>${product[1]}</td>
                                <td>${product[2]}</td>
                                <td>${product[3]}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm me-2">Delete</button>
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

    // function fetchProducts() {
    //     fetch('/editproducts')
    //         .then(response => response)

    // }

    // Fetch products on page load
    fetchProducts();

    // Add event listener to the refresh button
    refreshButton.addEventListener('click', fetchProducts);
});
