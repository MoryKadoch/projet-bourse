function addCours() {
    var selectCours = document.getElementById("select-cours");
    var selectedCours = selectCours.options[selectCours.selectedIndex].value;
    var coursName = selectCours.options[selectCours.selectedIndex].text;
    //encodedCoursName = encodeURIComponent(coursName);
    window.location.href = '/add?cours=' + selectedCours + '&name=' + coursName;
}

const deleteBtns = document.querySelectorAll('.btn-danger');
deleteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        console.log('Suppression du cours ' + btn.dataset.cours);
        const cours = btn.dataset.cours;
        fetch(`/delete`, { method: 'POST', body: JSON.stringify({ 'cours': cours }), headers: { 'Content-Type': 'application/json' } })
            .then(response =>
                window.location.href = '/'
            );
    });
});

const updateBtns = document.querySelectorAll('.update-btn');
updateBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        console.log('Mise à jour du cours ' + btn.dataset.cours);
        window.location.href = '/add?cours=' + btn.dataset.name + '&name=' + btn.dataset.cours;
    });
});