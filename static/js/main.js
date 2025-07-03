$(document).ready(function () {
	$('.salonsSlider').slick({
		arrows: true,
		slidesToShow: 4,
		infinite: true,
		prevArrow: $('.salons .leftArrow'),
		nextArrow: $('.salons .rightArrow'),
		responsive: [
			{
				breakpoint: 991,
				settings: {

					centerMode: true,
					//centerPadding: '60px',
					slidesToShow: 2
				}
			},
			{
				breakpoint: 575,
				settings: {
					slidesToShow: 1
				}
			}
		]
	});
	$('.servicesSlider').slick({
		arrows: true,
		slidesToShow: 4,
		prevArrow: $('.services .leftArrow'),
		nextArrow: $('.services .rightArrow'),
		responsive: [
			{
				breakpoint: 1199,
				settings: {


					slidesToShow: 3
				}
			},
			{
				breakpoint: 991,
				settings: {

					centerMode: true,
					//centerPadding: '60px',
					slidesToShow: 2
				}
			},
			{
				breakpoint: 575,
				settings: {
					slidesToShow: 1
				}
			}
		]
	});

	$('.mastersSlider').slick({
		arrows: true,
		slidesToShow: 4,
		prevArrow: $('.masters .leftArrow'),
		nextArrow: $('.masters .rightArrow'),
		responsive: [
			{
				breakpoint: 1199,
				settings: {


					slidesToShow: 3
				}
			},
			{
				breakpoint: 991,
				settings: {


					slidesToShow: 2
				}
			},
			{
				breakpoint: 575,
				settings: {
					slidesToShow: 1
				}
			}
		]
	});

	$('.reviewsSlider').slick({
		arrows: true,
		slidesToShow: 4,
		prevArrow: $('.reviews .leftArrow'),
		nextArrow: $('.reviews .rightArrow'),
		responsive: [
			{
				breakpoint: 1199,
				settings: {


					slidesToShow: 3
				}
			},
			{
				breakpoint: 991,
				settings: {


					slidesToShow: 2
				}
			},
			{
				breakpoint: 575,
				settings: {
					slidesToShow: 1
				}
			}
		]
	});

	// menu
	$('.header__mobMenu').click(function () {
		$('#mobMenu').show()
	})
	$('.mobMenuClose').click(function () {
		$('#mobMenu').hide()
	})
	var mySuccessHandler = createSuccessHandler();
	let picker = new AirDatepicker('#datepickerHere',
		{
			minDate: new Date(),
			maxDate: addOneMonthToCurrent(),
			onSelect({ date }) {
				let month = date.getMonth() + 1
				current_master_id = $('.accordion__block_master').attr('id')
				$.ajax({
					url: '/ajax_load_slots/',
					data: {
						'date': date.getFullYear() + "-" + month + "-" + date.getDate(),
						'specialist_id': current_master_id
					},
					success: mySuccessHandler
				})
			}

		})
	function addOneMonthToCurrent() {
		let now = new Date();
		return new Date(now.getFullYear(), now.getMonth() + 1, now.getDate());  // Добавляем 1 месяц
	}

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
		acc[i].addEventListener("click", function (e) {
			e.preventDefault()
			this.classList.toggle("active");
			var panel = $(this).next()
			panel.hasClass('active') ?
				panel.removeClass('active')
				:
				panel.addClass('active')
		});
	}

	$(document).on('click', '.ajax_service_salon', function (e) {
		current_service_id = $('.ajax_service_services').attr('id')
		current_master_id = $('.accordion__block_master').attr('id')
		$.ajax({
			url: '/ajax_load_salons/',
			data: {
				'specialist_id': current_master_id,
				'service_id': current_service_id

			},
			success: function (data) {
				$('.service__salons > .panel').html(data.template)
			}
		})
	})
	$(document).on('click', '.ajax_service_services', function (e) {
		current_salon_id = $('.ajax_service_salon').attr('id')
		current_master_id = $('.accordion__block_master').attr('id')
		console.log(current_salon_id)
		$.ajax({
			url: '/ajax_load_beauty_services/',
			data: {
				'salon_id': current_salon_id,
				'specialist_id': current_master_id
			},
			success: function (data) {
				$('.service__services > .panel').html(data.template)
			}
		})
	})

	$(document).on('click', '.ajax_service_masters', function (e) {
		current_salon_id = $('.ajax_service_salon').attr('id')
		current_service_id = $('.ajax_service_services').attr('id')
		time = $('.time__elems_btn.active').text()
		let data = {
			'salon_id': current_salon_id,
			'service_id': current_service_id,
			'time': time
		}
		if (picker.lastSelectedDate) {
			data['date'] = picker.lastSelectedDate.toDateString()
		}
		$.ajax({
			url: '/ajax_load_specialists/',
			data: data,
			success: function (data) {
				$('.service__masters > .panel').html(data.template)
			}
		})
	})

	$(document).on('click', '.accordion__block', function (e) {
		let thisName, thisAddress;

		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()
		thisId = $(this).find('> .accordion__block_intro').attr('id')
		console.log(thisName)
		if (thisId) {
			$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' + thisAddress).attr('id', thisId)
		}
		else {
			$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' + thisAddress).attr('id', null)
		}
		setTimeout(() => {
			$(this).parent().parent().find('> button.active').click()
		}, 200)

		// $(this).parent().addClass('hide')

		// console.log($(this).parent().parent().find('.panel').hasClass('selected'))

		// $(this).parent().parent().find('.panel').addClass('selected')
	})


	$('.accordion__block_item').click(function (e) {
		let thisName, thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' + thisAddress)
		// $(this).parent().parent().parent().parent().find('> button.active').click()
		// $(this).parent().parent().parent().addClass('hide')
		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})



	// 	console.log($('.service__masters > .panel').attr('data-masters'))
	// if($('.service__salons .accordion.selected').text() === "BeautyCity Пушкинская  ул. Пушкинская, д. 78А") {
	// }


	$(document).on('click', '.service__masters .accordion__block', function (e) {
		master_id = $(this)
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})

	// $('.accordion__block_item').click(function(e) {
	// 	const thisName = $(this).find('.accordion__block_item_intro').text()
	// 	const thisAddress = $(this).find('.accordion__block_item_address').text()
	// 	console.log($(this).parent().parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
	// })



	// $('.accordion__block_item').click(function(e) {
	// 	const thisChildName = $(this).text()
	// 	console.log(thisChildName)
	// 	console.log($(this).parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)

	// })
	// $('.accordion.selected').click(function() {
	// 	$(this).parent().find('.panel').hasClass('selected') ? 
	// 	 $(this).parent().find('.panel').removeClass('selected')
	// 		:
	// 	$(this).parent().find('.panel').addClass('selected')
	// })


	//popup
	$('.header__block_auth').click(function (e) {
		e.preventDefault()
		$('#authModal').arcticmodal();
		// $('#confirmModal').arcticmodal();

	})

	$('.rewiewPopupOpen').click(function (e) {
		e.preventDefault()
		$('#reviewModal').arcticmodal();
	})
	$('.payPopupOpen').click(function (e) {
		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.tipsPopupOpen').click(function (e) {
		e.preventDefault()
		$('#tipsModal').arcticmodal();
	})


	//service
	function createSuccessHandler() {
		return function (data) {
			{
				$('.time__elems').html(data.template)
				$('.time__items .time__elems_elem .time__elems_btn').click(function (e) {
					e.preventDefault()
					$('.time__elems_btn').removeClass('active')
					$(this).addClass('active')
					// $(this).hasClass('active') ? $(this).removeClass('active') : $(this).addClass('active')
				})
			}

		}
	}


	$(document).on('click', '.servicePage', function () {
		if ($('.time__items .time__elems_elem .time__elems_btn').hasClass('active') && $('.service__form_block > button').length === $('.service__form_block > button.selected').length) {
			$('.time__btns_next').addClass('active')
		}
	})



})