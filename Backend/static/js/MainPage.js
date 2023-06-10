
    // 공지사항 순서 변경 모달
    const Modal_reorder = document.getElementById("Modal_reorder");
    const btn_reorder_open = document.getElementById("Btn_Modal_reorder_open");
    const btn_reorder_close = document.getElementById("Btn_Modal_reorder_close");

    function open_reorder_modal() {
        Modal_reorder.style.display = "block";
        var stickyHeaders = document.querySelectorAll(".sticky-header");

    }

    function close_reorder_modal() {
        Modal_reorder.style.display = "none";

    }

    btn_reorder_open.addEventListener("click", open_reorder_modal)
    btn_reorder_close.addEventListener("click", close_reorder_modal)


    // 키워드 수정시 option에 따라서 기존 키워드 정보 출력 이건 뭘까...
    function changePlaceholder() {
        var select = document.getElementById("target_select");
        var input = document.getElementById("edit_keyword");
        var checkboxes = document.querySelectorAll(".cat-container input[type='checkbox']");
        var selectedOption = select.options[select.selectedIndex].value;

        input.value = selectedOption;

        checkboxes.forEach(function (checkbox) {
        checkbox.checked = checkbox.value === selectedOption ? true : false;
        });
    }

    // 키워드 추가 관련 모달
    const Modal_keyword_add = document.getElementById("Modal_keyword_add");
    const btn_keyword_add_open = document.getElementById("Btn_Modal_keyword_add_open");
    const btn_keyword_add_close = document.getElementById("Btn_Modal_keyword_add_close");

    function open_keyword_add_modal() {
        Modal_keyword_add.style.display = "block";

    }

    function close_keyword_add_modal() {
        Modal_keyword_add.style.display = "none";


    }

    btn_keyword_add_open.addEventListener("click", open_keyword_add_modal);
    btn_keyword_add_close.addEventListener("click", close_keyword_add_modal);

    function handleOptionSelection() {
        const selectedOptions = Array.from(document.querySelectorAll('.option')).map(select => select.value);
        const uniqueOptions = new Set(selectedOptions);

         // 중복된 옵션을 비활성화
        Array.from(document.querySelectorAll('.option option')).forEach(option => {
            if (uniqueOptions.has(option.value)) {
                option.disabled = true;
            } else {
                option.disabled = false;
            }
        });
    }

    // 각 키워드당 수정 모달창
    const buttons = document.querySelectorAll(".btn_keyedit");

    function openModal(modalId, i) {
        const Modal_keyword_edit = document.getElementById(modalId);
        const btn_keyword_edit_close = document.getElementById("Btn_Modal_keyword_edit_close"+(i+1));


        function open_keyword_edit_modal() {
            Modal_keyword_edit.style.display = "block";
        }

        function close_keyword_edit_modal() {
           Modal_keyword_edit.style.display = "none";
        }


        buttons[i].addEventListener("click", open_keyword_edit_modal);
        btn_keyword_edit_close.addEventListener("click", close_keyword_edit_modal);
    }

    for (var i = 0; i < buttons.length; i++) {
        var modalId = "Modal_keyword_edit" + (i + 1).toString();
        openModal(modalId, i);
    }

    // 모든 select 태그에 이벤트 핸들러 추가
    Array.from(document.querySelectorAll('.option')).forEach(select => {
        select.addEventListener('change', handleOptionSelection);
    });




    function submitForm() {
        var keyword = document.getElementById("keyword_input").value; // keyword_add input의 값 가져오기

        // 다른 form 태그의 input에 값을 설정
        document.getElementById("key_sim_input").value = keyword;

        // 다른 form 태그의 submit 호출
        document.getElementById("key_sim").submit();
    }



