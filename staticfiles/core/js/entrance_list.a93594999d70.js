'use strict'

const tableBody = document.querySelector('.client-table-body');
const searchForm = document.querySelector('.search-client-form');
const csrfToken = searchForm.querySelector('input[name="csrfmiddlewaretoken"]').value;


tableBody.addEventListener('click', async (evt) => {

    const deleteBtn = evt.target.closest('.delete-bt');
    if (!deleteBtn) return;

    const row = deleteBtn.closest('tr');

    // Rows info
    const name = row.cells[0].innerText;
    const cpf = row.cells[1].innerText;
    const time = row.cells[6].querySelector('span') ? row.cells[6].querySelector('span').innerText : row.cells[6].innerText;

    // Confirmation msg
    const message = `Tem certeza que deseja excluir este registro?\n\nNome: ${name}\nCPF: ${cpf}\nHorário: ${time}`;

    if (confirm(message)) {

        const idToDelete = deleteBtn.dataset.id;

        try {
            const response = await fetch(`${window.location.origin}/system/cancel/${idToDelete}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            });

            if (response.ok) {
                window.location.reload();
            } else {
                alert("Erro ao excluir o registro.");
            }
        } catch (e) {
            console.error(e);
            alert("Erro de conexão.");
        }
    }
});