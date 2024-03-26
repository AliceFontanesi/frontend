function editProduct(productId) {
    const newName = prompt("Inserisci il nuovo nome del prodotto:");
    const newPrice = parseFloat(prompt("Inserisci il nuovo prezzo del prodotto:"));

    if (newName && !isNaN(newPrice)) {
        const data = {
            data: {
                attributes: {
                    nome: newName,
                    prezzo: newPrice
                }
            }
        };

        fetch(`http://localhost:8000/products/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            alert("Prodotto modificato con successo!");
            // implementare un'altra logica per aggiornare solo il prodotto modificato senza dover ricaricare tutti i prodotti
        })
        .catch(error => {
            console.error('Errore:', error);
        });
    } else {
        alert("Nome o prezzo non validi.");
    }
}