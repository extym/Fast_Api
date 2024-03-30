$(document).ready(function () {
    const pieChartBaseSettings = {
        type: 'doughnut',
        data: {
            datasets: [{
                data: null,
                backgroundColor: null,
            }],
            labels: null,
        },
        options: {
            cutoutPercentage: 75,
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false,
                position: 'top',
            },
            title: {
                display: false,
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            tooltips: {
                enabled: true,
                intersect: false,
                theme: 'light',
                mode: 'nearest',
                bodySpacing: 5,
                yPadding: 5,
                xPadding: 5,
                caretPadding: 0,
                displayColors: false,
                // backgroundColor: KTApp.getSettings()['colors']['theme']['base']['primary'],
                // titleFontColor: '#ffffff',
                cornerRadius: 4,
                footerSpacing: 0,
                titleSpacing: 0,
            }
        }
    };

    initPieCharts();
    initSlider();
    initOptionsTippy();

    $(document).on('pjax:end', function () {
        initPieCharts();
        initSlider();
        initOptionsTippy();
    });


    function initSlider() {
        var swiper = new Swiper(".swiper", {
            slidesPerView: 1,
            slidesPerGroup: 1,
            // simulateTouch: false,
            spaceBetween: 20,
            // allowTouchMove: false,
            // noSwiping: true,
            // resistance: true,
            // resistanceRatio: 0,
            // mousewheel: true,
            breakpoints: {
                1500: {
                    slidesPerView: 2,
                },
                1920: {
                    slidesPerView: 2,
                },
                2000: {
                    slidesPerView: 3,
                },
                3840: {
                    slidesPerView: 5
                }
            },
            pagination: {
                el: ".swiper-pagination",
                dynamicBullets: true,
                clickable: true,
            },
            mousewheel: {
                forceToAxis: true,
                sensitivity: 1,
                releaseOnEdges: true,
            },
        });

        swiper.on('slideChange', function (e) {
            return false;
            // swiper.stopPropagation();
        });
        // document.querySelector('.swiper').addEventListener('mousewheel', function(e){
        // console.log(123);
        // });
    }

    function initOptionsTippy() {
        $('.openChartOptions').each(function (i, obj) {
            let chart = $(this).closest('.chart-card');
            let chartOptionsContent = chart.find('input[name="tippy_chartOptions"]').val();

            tippy($(obj)[0], {
                content: chartOptionsContent,
                allowHTML: true,
                interactive: true,
                theme: 'light',
                placement: 'top',
                trigger: 'click'
            });
        });
    }

    function initPieCharts() {
        let pieCharts = $('.pieChartCanvas');

        pieCharts.each(function (i, obj) {
            let config = JSON.parse(JSON.stringify(pieChartBaseSettings));
            let chartInput = $(this).closest('.chart-card').find('input[name="chartData"]');

            let chartData = JSON.parse(chartInput.val());

            if (!$.isEmptyObject(chartData)) {

                let labels = [];
                let dataset = [];
                let colors = [];

                $.each(chartData.data.accounts, function (label, account) {
                    labels.push(label);
                    colors.push(account.color);

                    if (chartData.info.type === 'currency') {
                        if (chartData.info.expensesSwitch) {
                            dataset.push(account.value.RUB.actual.withoutExpenses);
                        } else {
                            dataset.push(account.value.RUB.actual);
                        }
                    } else {
                        dataset.push(account.value.actual);
                    }
                });

                config.data.datasets[0].data = dataset;
                config.data.datasets[0].backgroundColor = colors;
                config.data.labels = labels;

                var ctx = obj.getContext('2d');
                var pieChart = new Chart(ctx, config);
            }
        });
    }


    $(document).on('change', 'input[name="considerExpenses"]', function (e) {

        let chart = $(this).closest('.chart-card');
        let currencySwitch = chart.find('.currencySwitch');

        let chartData = JSON.parse(chart.find('input[name="chartData"]').val());
        let accounts = chart.find('.detailedByAccounts .account');

        // Get current currency
        // let currentCurrencyItem = chart.find('input[name="currency"]').val();

        let currentCurrencyItem = currencySwitch.find('.active');
        let currencyCode = currentCurrencyItem.attr('data-code');
        let currencySymbol = currentCurrencyItem.attr('data-symbol');

        if (!$.isEmptyObject(chartData)) {
            // Set total value
            if ($(this).is(':checked')) {
                chart.find('.totalValue').text(parseInt(chartData['data']['total']['value'][currencyCode]['actual']['withExpenses']).toLocaleString('ru') + ' ' + currencySymbol);

                accounts.each(function (i, obj) {
                    let label = $(obj).data('label');

                    if (chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withExpenses']) {
                        let actual = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withExpenses']).toLocaleString('ru')
                        $(obj).find('.value').text(actual + ' ' + chartData['info']['datasetSymbol']);

                        if (chartData['data']['accounts'][label]['value'][currencyCode]['previous']) {
                            let previous = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['difference']['withExpenses']).toLocaleString('ru')
                            $(obj).find('.diffValue').text(previous + ' ' + chartData['info']['datasetSymbol']);
                        }
                    }
                });
            } else {
                chart.find('.totalValue').text(parseInt(chartData['data']['total']['value'][currencyCode]['actual']['withoutExpenses']).toLocaleString('ru') + ' ' + currencySymbol);

                accounts.each(function (i, obj) {
                    let label = $(obj).data('label');

                    if (chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withoutExpenses']) {
                        let actual = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withoutExpenses']).toLocaleString('ru')
                        $(obj).find('.value').text(actual + ' ' + chartData['info']['datasetSymbol']);

                        if (chartData['data']['accounts'][label]['value'][currencyCode]['previous']['difference']) {
                            let previous = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['previous']['difference']['withoutExpenses']).toLocaleString('ru')
                            $(obj).find('.diffValue').text(previous + ' ' + chartData['info']['datasetSymbol']);
                        }
                    }
                });
            }
        }
    });


    const currencySwitchItem = ".currencySwitch .item";

    $(document).on('click', currencySwitchItem, function () {
        let chart = $(this).closest('.chart-card');
        let currencySwitch = chart.find('.currencySwitch');

        // Add active class
        chart.find(currencySwitchItem).removeClass('active');
        $(this).addClass('active');

        let currencyCode = $(this).data('code');
        let currencySymbol = $(this).data('symbol');

        // Change data attr of selected currency
        currencySwitch.attr('data-currency', currencyCode);

        // Get expenses status
        let considerExpensesSwitch = chart.find('input[name="considerExpenses"]');
        let hasExpensesOption = false;
        let withExpenses = false;

        if (considerExpensesSwitch.length) {
            hasExpensesOption = true;

            if (considerExpensesSwitch.is(':checked')) {
                withExpenses = true;
            }
        }

        if (currencyCode && currencySymbol) {
            let chartData = JSON.parse(chart.find('input[name="chartData"]').val());
            let accounts = chart.find('.detailedByAccounts .account');

            if (!$.isEmptyObject(chartData)) {
                // Set total value
                if (!hasExpensesOption) {
                    chart.find('.totalValue').text(parseInt(chartData['data']['total']['value'][currencyCode]['actual']).toLocaleString('ru') + ' ' + currencySymbol);

                    accounts.each(function (i, obj) {
                        let label = $(obj).data('label');

                        if (chartData['data']['accounts'][label]['value'][currencyCode]['actual']) {
                            let actual = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['actual']).toLocaleString('ru')
                            $(obj).find('.value').text(actual + ' ' + currencySymbol);

                            if (chartData['data']['accounts'][label]['value'][currencyCode]['difference']) {
                                let previous = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['difference']).toLocaleString('ru')
                                $(obj).find('.diffValue').text(previous + ' ' + currencySymbol);
                            }
                        }
                    });
                } else {
                    if (withExpenses) {
                        chart.find('.totalValue').text(parseInt(chartData['data']['total']['value'][currencyCode]['actual']['withExpenses']).toLocaleString('ru') + ' ' + currencySymbol);

                        accounts.each(function (i, obj) {
                            let label = $(obj).data('label');

                            if (chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withExpenses']) {
                                let actual = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withExpenses']).toLocaleString('ru')
                                $(obj).find('.value').text(actual + ' ' + currencySymbol);

                                if (chartData['data']['accounts'][label]['value'][currencyCode]['difference']) {
                                    let previous = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['difference']['withExpenses']).toLocaleString('ru')
                                    $(obj).find('.diffValue').text(previous + ' ' + currencySymbol);
                                }
                            }
                        });
                    }
                    else  {
                        chart.find('.totalValue').text(parseInt(chartData['data']['total']['value'][currencyCode]['actual']['withoutExpenses']).toLocaleString('ru') + ' ' + currencySymbol);

                        accounts.each(function (i, obj) {
                            let label = $(obj).data('label');

                            if (chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withoutExpenses']) {
                                let actual = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['actual']['withoutExpenses']).toLocaleString('ru')
                                $(obj).find('.value').text(actual + ' ' + currencySymbol);

                                if (chartData['data']['accounts'][label]['value'][currencyCode]['difference']) {
                                    let previous = parseFloat(chartData['data']['accounts'][label]['value'][currencyCode]['difference']['withoutExpenses']).toLocaleString('ru')
                                    $(obj).find('.diffValue').text(previous + ' ' + currencySymbol);
                                }
                            }
                        });
                    }
                }
            }
        }
    });
});