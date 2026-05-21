/**
 * MarketList - Archived History Management
 * Selección y borrado masivo de listas archivadas pasadas.
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
        btn.innerHTML = '<i class="bi bi-pencil-square me-1 text-primary"></i> Seleccionar listas';
    }

    document.querySelectorAll('.check-container').forEach(el => el.classList.toggle('d-none', !isEditModeActive));
    document.querySelectorAll('.individual-actions').forEach(el => el.classList.toggle('d-none', isEditModeActive));

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
        const cb = element.querySelector('.lista-checkbox');
        if (cb) {
            cb.checked = !cb.checked;
            updateCount();
        }
    } else {
        updateCount();
    }
}

function toggleAll(source) {
    const checkboxes = document.querySelectorAll('.lista-checkbox');
    checkboxes.forEach(cb => cb.checked = source.checked);
    updateCount();
}

function updateCount() {
    const checkboxes = document.querySelectorAll('.lista-checkbox:checked');
    const checkedCount = checkboxes.length;

    const countBadge = document.getElementById('countSelected');
    const deleteBtn = document.querySelector('#floatingDeleteBar button');

    if (countBadge) countBadge.innerText = checkedCount;
    if (deleteBtn) deleteBtn.disabled = (checkedCount === 0);

    document.querySelectorAll('.item-seleccionable').forEach(item => {
        const cb = item.querySelector('.lista-checkbox');
        if (cb) {
            item.style.transform = cb.checked ? 'scale(0.98)' : 'scale(1)';
            item.style.opacity = cb.checked ? '0.8' : '1';
        }
    });
}

function showDeleteModal() {
    const checkedCount = document.querySelectorAll('.lista-checkbox:checked').length;
    const modalCountLabel = document.getElementById('modalCount');
    if (modalCountLabel) modalCountLabel.innerText = checkedCount;

    const modalElement = document.getElementById('modalConfirmMultiple');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

// Envío del formulario definitivo
function submitMultipleDelete() {
    const form = document.getElementById('formDeleteMultiple');
    if (form) form.submit();
}