(function () {

    let isSetupForMobile = false;

    function isMobile() {
        return window.matchMedia("(max-width: 900px)").matches;
    }

    function reportWindowSize() {
        // not applicable for compact prompt layout
        if (gradioApp().querySelector('.toprow-compact-tools')) return;

        let currentlyMobile = isMobile();
        if (currentlyMobile == isSetupForMobile) return;
        isSetupForMobile = currentlyMobile;

        for (let tab of ["txt2img", "img2img"]) {
            let button = gradioApp().getElementById(tab + '_generate_box');
            let target = gradioApp().getElementById(tab + '_actions_column');
            if (button && target && button.parentElement !== target) {
                target.insertBefore(button, target.firstElementChild);
            }

            let results = gradioApp().getElementById(tab + '_results');
            if (results) {
                results.classList.toggle('mobile', currentlyMobile);
            }
        }
    }

    window.addEventListener("resize", reportWindowSize);

    onUiLoaded(function () {
        reportWindowSize();
    });

})();
