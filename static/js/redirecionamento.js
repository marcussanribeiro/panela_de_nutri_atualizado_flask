
function editar(id) {
    window.location.href = "/staffer/editar_post/" + id;
}
function deletar(id) {
    if(confirm("Deseja deletar?")) {
      var form = document.createElement('form');
      form.setAttribute('method', 'POST');
      form.setAttribute('action', '/staffer/deletar/' + id);
      document.body.appendChild(form);
      form.submit();
    }
  }