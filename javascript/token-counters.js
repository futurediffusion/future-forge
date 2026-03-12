let promptTokenCountUpdateFunctions = {};
let tokenCounterBindings = {};

function getTxt2imgPromptIdsForCounters() {
    return opts.txt2img_show_future_tab
        ? ["txt2img_future_prompt", "txt2img_prompt"]
        : ["txt2img_prompt", "txt2img_future_prompt"];
}

function resolvePromptId(ids) {
    return ids.find((id) => gradioApp().getElementById(id));
}

function update_txt2img_tokens(...args) {
    // Called from Gradio
    update_token_counter("txt2img_token_button");
    update_token_counter("txt2img_negative_token_button");
    if (args.length == 2) {
        return args[0];
    }
    return args;
}

function update_img2img_tokens(...args) {
    // Called from Gradio
    update_token_counter("img2img_token_button");
    update_token_counter("img2img_negative_token_button");
    if (args.length == 2) {
        return args[0];
    }
    return args;
}

function update_token_counter(button_id) {
    promptTokenCountUpdateFunctions[button_id]?.();
}

function recalculatePromptTokens(name) {
    promptTokenCountUpdateFunctions[name]?.();
}

function recalculate_prompts_txt2img() {
    // Called from Gradio
    for (const id of getTxt2imgPromptIdsForCounters()) {
        recalculatePromptTokens(id);
    }
    recalculatePromptTokens("txt2img_neg_prompt");
    return Array.from(arguments);
}

function recalculate_prompts_img2img() {
    // Called from Gradio
    recalculatePromptTokens("img2img_prompt");
    recalculatePromptTokens("img2img_neg_prompt");
    return Array.from(arguments);
}

function setupTokenCounting(id, id_counter, id_button) {
    let prompt = gradioApp().getElementById(id);
    let counter = gradioApp().getElementById(id_counter);
    let textarea = gradioApp().querySelector(`#${id} > label > textarea`);

    if (!prompt || !counter || !textarea) {
        return;
    }

    let existingBinding = tokenCounterBindings[id_button];
    if (existingBinding?.textarea === textarea) {
        return;
    }

    if (existingBinding?.textarea) {
        existingBinding.textarea.removeEventListener("input", existingBinding.func);
    }

    if (counter.parentElement == prompt.parentElement) {
        return;
    }

    prompt.parentElement.insertBefore(counter, prompt);
    prompt.parentElement.style.position = "relative";

    let func = onEdit(id, textarea, 800, function () {
        if (counter.classList.contains("token-counter-visible")) {
            gradioApp().getElementById(id_button)?.click();
        }
    });

    tokenCounterBindings[id_button] = {
        textarea,
        func,
    };

    promptTokenCountUpdateFunctions[id] = func;
    promptTokenCountUpdateFunctions[id_button] = func;
}

function toggleTokenCountingVisibility(id, id_counter, id_button) {
    let counter = gradioApp().getElementById(id_counter);

    counter.style.display = opts.disable_token_counters ? "none" : "block";
    counter.classList.toggle(
        "token-counter-visible",
        !opts.disable_token_counters,
    );
}

function runCodeForTokenCounters(fun) {
    let txt2imgPromptId = resolvePromptId(getTxt2imgPromptIdsForCounters());
    if (txt2imgPromptId) {
        fun(txt2imgPromptId, "txt2img_token_counter", "txt2img_token_button");
    }
    fun(
        "txt2img_neg_prompt",
        "txt2img_negative_token_counter",
        "txt2img_negative_token_button",
    );
    fun("img2img_prompt", "img2img_token_counter", "img2img_token_button");
    fun(
        "img2img_neg_prompt",
        "img2img_negative_token_counter",
        "img2img_negative_token_button",
    );
}

onUiLoaded(function () {
    runCodeForTokenCounters(setupTokenCounting);
});

onOptionsChanged(function () {
    runCodeForTokenCounters(toggleTokenCountingVisibility);
});
