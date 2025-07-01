document.querySelectorAll('.rewiewPopupOpen').forEach(link => {
  link.addEventListener('click', () => {
    const modal = document.getElementById('reviewModal');

    const name = link.dataset.name;
    const phone = link.dataset.phone;
    const date = link.dataset.date;

    modal.querySelector('input[name="name"]').value = name;
    modal.querySelector('input[name="phone_number"]').value = phone;
    modal.querySelector('input[name="dateVis"]').value = date;
  });
});