function showProduct(productId) {
    fetch(`http://localhost:8000/products/${productId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            // Mostra i dettagli del prodotto in un modale
            alert(`Dettagli prodotto:\nID: ${data.data.id}\nMarca: ${data.data.attributes.marca}\nNome: ${data.data.attributes.nome}\nPrezzo: ${data.data.attributes.prezzo}`);
        })
        .catch(error => {
            console.error('Errore:', error);
        });
}




