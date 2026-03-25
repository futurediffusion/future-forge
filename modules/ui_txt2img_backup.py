    with gr.Blocks(analytics_enabled=False, head=canvas_head) as txt2img_interface:
        toprow = ui_toprow.Toprow(is_img2img=False, is_compact=False) # Creado al inicio para evitar errores de variable
        
        dummy_component = gr.Textbox(visible=False)
        dummy_component_number = gr.Number(visible=False)

        future_prompt = toprow.prompt
        future_submit = toprow.submit

        with gr.Accordion("Advanced", open=False, elem_id="txt2img_advanced_accordion"):
            extra_tabs = gr.Tabs(elem_id="txt2img_extra_tabs", elem_classes=["extra-networks"])
            extra_tabs.__enter__()

            with gr.Tab("Generation", id="txt2img_generation") as txt2img_generation_tab:
                with ResizeHandleRow(equal_height=False):
                    with ExitStack() as stack:
                        if shared.opts.txt2img_settings_accordion:
                            stack.enter_context(gr.Accordion("Open for Settings", open=False))
                        txt2img_settings_column = stack.enter_context(gr.Column(variant="compact", elem_id="txt2img_settings"))
    
                        scripts.scripts_txt2img.prepare_ui()
    
                        for category in ordered_ui_categories():
                            with txt2img_settings_column:
                                if category == "prompt":
                                    pass # Los prompts se renderizarán abajo
    
                                elif category == "dimensions":
                                    with FormRow():
                                        with gr.Column(elem_id="txt2img_column_size", scale=4):
                                            width = gr.Slider(minimum=64, maximum=2048, step=64, label="Width", value=1024, elem_id="txt2img_width")
                                            height = gr.Slider(minimum=64, maximum=2048, step=64, label="Height", value=1024, elem_id="txt2img_height")
    
                                        with gr.Column(elem_id="txt2img_dimensions_row", scale=1, elem_classes="dimensions-tools"):
                                            res_switch_btn = ToolButton(value=switch_values_symbol, elem_id="txt2img_res_switch_btn", tooltip="Switch width/height")
    
                                        if opts.dimensions_and_batch_together:
                                            with gr.Column(elem_id="txt2img_column_batch"):
                                                batch_count = gr.Slider(minimum=1, maximum=128, step=1, label="Batch Count", value=1, elem_id="txt2img_batch_count")
                                                batch_size = gr.Slider(minimum=1, maximum=8, step=1, label="Batch Size", value=1, elem_id="txt2img_batch_size")
    
                                elif category == "cfg":
                                    with gr.Row():
                                        distilled_cfg_scale = gr.Slider(minimum=1.0, maximum=24.0, step=0.5, label="Distilled CFG Scale", value=3.0, elem_id="txt2img_distilled_cfg_scale", scale=4)
                                        cfg_scale = gr.Slider(minimum=1.0, maximum=24.0, step=0.5, label="CFG Scale", value=6.0, elem_id="txt2img_cfg_scale", scale=4)
                                        cfg_scale.change(lambda v: gr.update(interactive=(v > 1.0)), inputs=[cfg_scale], outputs=[toprow.negative_prompt], queue=False, show_progress=False)
                                        scripts.scripts_txt2img.setup_ui_for_section(category)
    
                                elif category == "accordions":
                                    with gr.Row(elem_id="txt2img_accordions", elem_classes="accordions"):
                                        with InputAccordion(False, label="Hires. fix", elem_id="txt2img_hr") as enable_hr:
                                            with enable_hr.extra():
                                                hr_final_resolution = FormHTML(value="", elem_id="txtimg_hr_finalres", label="Upscaled resolution")
        
                                        with FormRow(elem_id="txt2img_hires_fix_row1", variant="compact"):
                                            hr_upscaler = gr.Dropdown(label="Upscaler", elem_id="txt2img_hr_upscaler", choices=[*shared.latent_upscale_modes, *[x.name for x in shared.sd_upscalers]], value=shared.latent_upscale_default_mode)
                                            hr_second_pass_steps = gr.Slider(minimum=0, maximum=150, step=1, label="Hires steps", value=0, elem_id="txt2img_hires_steps")
                                            denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.05, label="Denoising strength", value=0.6, elem_id="txt2img_denoising_strength")
        
                                        with FormRow(elem_id="txt2img_hires_fix_row2", variant="compact"):
                                            hr_scale = gr.Slider(minimum=1.0, maximum=4.0, step=0.05, label="Upscale by", value=2.0, elem_id="txt2img_hr_scale")
                                            hr_resize_x = gr.Slider(minimum=0, maximum=4096, step=64, label="Resize width to", value=0, elem_id="txt2img_hr_resize_x")
                                            hr_resize_y = gr.Slider(minimum=0, maximum=4096, step=64, label="Resize height to", value=0, elem_id="txt2img_hr_resize_y")
        
                                        with FormRow(elem_id="txt2img_hires_fix_row_cfg", variant="compact"):
                                            hr_distilled_cfg = gr.Slider(minimum=1.0, maximum=24.0, step=0.5, label="Hires Distilled CFG Scale", value=3.0, elem_id="txt2img_hr_distilled_cfg")
                                            hr_cfg = gr.Slider(minimum=1.0, maximum=24.0, step=0.5, label="Hires CFG Scale", value=6.0, elem_id="txt2img_hr_cfg")
        
                                        with FormRow(elem_id="txt2img_hires_fix_row3", variant="compact", visible=shared.opts.hires_fix_show_sampler) as hr_checkpoint_container:
                                            hr_checkpoint_name = gr.Dropdown(label="Hires Checkpoint", elem_id="hr_checkpoint", choices=["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True), value="Use same checkpoint", scale=2)
        
                                            hr_checkpoint_refresh = ToolButton(value=refresh_symbol)
        
                                            def get_additional_modules():
                                                modules_list = ["Use same choices"]
                                                if main_entry.module_list == {}:
                                                    _, modules = main_entry.refresh_models()
                                                    modules_list += list(modules)
                                                else:
                                                    modules_list += list(main_entry.module_list.keys())
                                                return modules_list
        
                                            modules_list = get_additional_modules()
        
                                            def refresh_model_and_modules():
                                                modules_list = get_additional_modules()
                                                return gr.update(choices=["Use same checkpoint"] + modules.sd_models.checkpoint_tiles(use_short=True)), gr.update(choices=modules_list)
        
                                            hr_additional_modules = gr.Dropdown(label="Hires VAE / Text Encoder", elem_id="hr_vae_te", choices=modules_list, value=["Use same choices"], multiselect=True, scale=3)
        
                                            hr_checkpoint_refresh.click(fn=refresh_model_and_modules, outputs=[hr_checkpoint_name, hr_additional_modules], show_progress=False)
        
                                        with FormRow(elem_id="txt2img_hires_fix_row3b", variant="compact", visible=shared.opts.hires_fix_show_sampler) as hr_sampler_container:
                                            hr_sampler_name = gr.Dropdown(label="Hires sampling method", elem_id="hr_sampler", choices=["Use same sampler"] + sd_samplers.visible_sampler_names(), value="Use same sampler")
                                            hr_scheduler = gr.Dropdown(label="Hires schedule type", elem_id="hr_scheduler", choices=["Use same scheduler"] + [x.label for x in sd_schedulers.schedulers], value="Use same scheduler")
        
                                        with FormRow(elem_id="txt2img_hires_fix_row4", variant="compact", visible=shared.opts.hires_fix_show_prompts) as hr_prompts_container:
                                            with gr.Column():
                                                hr_prompt = gr.Textbox(label="Hires prompt", elem_id="hires_prompt", show_label=False, lines=3, placeholder="Prompt for hires fix pass.\nLeave empty to use the same prompt as in first pass.", elem_classes=["prompt"])
                                            with gr.Column():
                                                hr_negative_prompt = gr.Textbox(label="Hires negative prompt", elem_id="hires_neg_prompt", show_label=False, lines=3, placeholder="Negative prompt for hires fix pass.\nLeave empty to use the same negative prompt as in first pass.", elem_classes=["prompt"])
        
                                        hr_cfg.change(lambda v: gr.update(interactive=(v > 1.0)), inputs=[hr_cfg], outputs=[hr_negative_prompt], queue=False, show_progress=False)
        
                                        scripts.scripts_txt2img.setup_ui_for_section(category)
    
                                elif category == "batch":
                                    if not opts.dimensions_and_batch_together:
                                        with FormRow(elem_id="txt2img_column_batch"):
                                            batch_count = gr.Slider(minimum=1, maximum=128, step=1, label="Batch Count", value=1, elem_id="txt2img_batch_count")
                                            batch_size = gr.Slider(minimum=1, maximum=8, step=1, label="Batch Size", value=1, elem_id="txt2img_batch_size")
    
                                elif category == "override_settings":
                                    with FormRow(elem_id="txt2img_override_settings_row") as row:
                                        override_settings = create_override_settings_dropdown("txt2img", row)
    
                                elif category == "scripts":
                                    with FormGroup(elem_id="txt2img_script_container"):
                                        custom_inputs = scripts.scripts_txt2img.setup_ui()
    
                                if category not in {"accordions", "cfg"}:
                                    scripts.scripts_txt2img.setup_ui_for_section(category)
    
                    with gr.Column(elem_id="txt2img_results_column"):
                        output_panel = create_output_panel("txt2img", opts.outdir_txt2img_samples)
                        
                        # RENDERIZADO MANUAL DEL TOPROW AQUÍ (DEBAJO DE RESULTADOS)
                        toprow.render() 
