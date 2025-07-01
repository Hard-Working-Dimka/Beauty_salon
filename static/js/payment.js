document.addEventListener('DOMContentLoaded', function () {
  const payButtons = document.querySelectorAll('.payPopupOpen');
  const inputAppointment = document.getElementById('appointment_id_input');
  const inputTips = document.getElementById('tips_amount_input');
  const paymentModal = document.getElementById('paymentModal');
  const tipsForm = document.querySelector('.tipsPopup__form');
  const tipsInput = tipsForm.querySelector('input[type="text"]');

  payButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const id = button.getAttribute('data-id');
      inputAppointment.value = id;
      inputTips.value = '';
      $(paymentModal).arcticmodal();
    });
  });

  tipsForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const tipsValue = tipsInput.value;

    if (!tipsValue || isNaN(tipsValue)) {
      alert('Введите корректную сумму');
      return;
    }

    inputAppointment.value = '';
    inputTips.value = tipsValue;
    $.arcticmodal('close');
    $(paymentModal).arcticmodal();
  });
});
