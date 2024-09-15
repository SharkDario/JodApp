document.addEventListener("DOMContentLoaded", function () {
    const tipoField = document.querySelector("select[name=_tipo]");
    if (tipoField) {
        tipoField.addEventListener("change", function () {
            // Recargar el formulario cuando el tipo cambie
            this.form.submit();
        });
    }
});