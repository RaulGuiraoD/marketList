/**
 * MarketList - Catalog Management
 * Selección masiva y eliminación de productos del catálogo.
 */

let isEditModeActive = false;

function toggleEditMode() {
    isEditModeActive = !isEditModeActive;

    const selectionTools = document.getElementById('selectionTools');
    const floatingBar = document.getElementById('floatingDeleteBar');
    const btn = document.getElementById('btnEditMode');

    if (!selectionTools || !floatingBar || !btn) return;

    selectionTools.classList.toggle('d-none', !isEditModeActive);
    floatingBar.classList.toggle('d-none', !isEditModeActive);

    if (isEditModeActive) {
        btn.innerHTML = '<i class="bi bi-x-lg me-1 text-danger"></i> Cancelar';
    } else {
        btn.innerHTML = '<i class="bi bi-pencil-square me-1 text-primary"></i> Seleccionar productos';
    }

    document.querySelectorAll('.check-container').forEach(el => el.classList.toggle('d-none', !isEditModeActive));
    document.querySelectorAll('.individual-delete').forEach(el => el.classList.toggle('d-none', isEditModeActive));

    if (!isEditModeActive) {
        const selectAllCheck = document.getElementById('selectAll');
        if (selectAllCheck) {
            selectAllCheck.checked = false;
            toggleAll(selectAllCheck);
        }
    }
}

function handleItemClick(event, element) {
    if (!isEditModeActive) return;

    if (event.target.tagName === 'A' || event.target.tagName === 'BUTTON' || event.target.closest('button')) {
        return;
    }

    if (event.target.type !== 'checkbox') {
        const cb = element.querySelector('.producto-checkbox');
        if (cb) {
            cb.checked = !cb.checked;
            updateCount();
        }
    } else {
        updateCount();
    }
}

function toggleAll(source) {
    const checkboxes = document.querySelectorAll('.producto-checkbox');
    checkboxes.forEach(cb => cb.checked = source.checked);
    updateCount();
}

function updateCount() {
    const checkboxes = document.querySelectorAll('.producto-checkbox:checked');
    const checkedCount = checkboxes.length;

    const countBadge = document.getElementById('countSelected');
    const deleteBtn = document.querySelector('#floatingDeleteBar button');

    if (countBadge) countBadge.innerText = checkedCount;
    if (deleteBtn) deleteBtn.disabled = (checkedCount === 0);

    document.querySelectorAll('.item-maestro').forEach(item => {
        const cb = item.querySelector('.producto-checkbox');
        if (cb) {
            item.style.backgroundColor = cb.checked ? 'rgba(13, 110, 253, 0.05)' : 'transparent';
        }
    });
}

function showDeleteModal() {
    const checkedCount = document.querySelectorAll('.producto-checkbox:checked').length;
    const modalCountLabel = document.getElementById('modalCount');
    if (modalCountLabel) modalCountLabel.innerText = checkedCount;

    const modalElement = document.getElementById('modalConfirmMultiple');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

function submitMultipleDelete() {
    const form = document.getElementById('formDeleteMultiple');
    if (form) form.submit();
}

function confirmDeleteIndividual(event, button, message) {
    event.stopPropagation(); // Evita que se active el modo selección del item de la lista
    if (confirm(message)) {
        // Obtiene la URL guardada en el atributo data-url y redirige o procesa mediante POST
        const url = button.getAttribute('data-url');
        
        // Forma limpia recomendada: Crear un formulario temporal e inyectarle el CSRF token para hacer POST seguro
        const tempForm = document.createElement('form');
        tempForm.method = 'POST';
        tempForm.action = url;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        
        tempForm.appendChild(csrfInput);
        document.body.appendChild(tempForm);
        tempForm.submit();
    }
}