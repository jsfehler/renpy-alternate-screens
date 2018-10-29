# Style for the title frame
style slot_quick_auto_title_frame:
    background gui.accent_color
    xsize gui.slot_button_width
    ysize gui.slot_button_height
    margin (0, 10, gui.slot_spacing / 2, 52)


# Style for the hbox inside the title frame 
style slot_quick_auto_title_frame_hbox:
    xalign 0.5
    yalign 0.95


style slot_quick_auto_button is slot_button
style slot_quick_auto_text is slot_button_text
style slot_quick_auto_time_text is slot_time_text
style slot_quick_auto_name_text is slot_name_text


# Screen for the Quick / Auto buttons
screen quick_auto_button(slot_amount, page_type):
    for i in range(slot_amount):
        $ slot = i + 1
        button:
            style_prefix "slot_quick_auto"
            action FileAction(slot, page=page_type)
            
            has vbox
            add FileScreenshot(slot, page=page_type) xalign 0.5
            
            text FileTime(slot, page=page_type, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                style "slot_quick_auto_time_text"
                

            text FileSaveName(slot, page=page_type):
                style "slot_quick_auto_name_text"

            key "save_delete" action FileDelete(slot, page=page_type)


# Screen for the Quick / Auto page
screen quick_auto_file_slots():
    hbox:
        vbox:
            frame:
                style "slot_quick_auto_title_frame"
                hbox:
                    style "slot_quick_auto_title_frame_hbox"
                    text _("Quick saves")
                    text _(" >")

            frame:
                style "slot_quick_auto_title_frame"
                hbox:
                    style "slot_quick_auto_title_frame_hbox"
                    text _("Automatic saves")
                    text _(" >")


        viewport:
            scrollbars "horizontal"
            mousewheel True
            draggable True
            edgescroll (gui.slot_button_width / 3, gui.slot_button_width * config.quicksave_slots)
            xalign 0.5
            yalign 0.5
            spacing gui.slot_spacing
            viewport_yfill False
            
            vbox:
                hbox:
                    use quick_auto_button(config.quicksave_slots, "quick")
                hbox:
                    use quick_auto_button(config.autosave_slots, "auto")


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:
            if persistent._file_page == "quick":
            ## Use the Quick / Auto page
                vbox:
                    frame:
                        ysize 60
                        background None

                    spacing gui.slot_spacing
                    use quick_auto_file_slots

            else:
                ## This ensures the input will get the enter event before any of the
                ## buttons do.
                order_reverse True

                ## The page name, which can be edited by clicking on a button.
                button:
                    style "page_label"

                    key_events True
                    xalign 0.5
                    action page_name_value.Toggle()

                    input:
                        style "page_label_text"
                        value page_name_value
            
                ## The grid of file slots.
                grid gui.file_slot_cols gui.file_slot_rows:
                    style_prefix "slot"

                    xalign 0.5
                    yalign 0.5

                    spacing gui.slot_spacing

                    use quick_auto_button(gui.file_slot_cols * gui.file_slot_rows, None)


            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                if persistent._file_page != "quick":
                    textbutton _("<") action FilePagePrevious()
                else:
                    textbutton _("<")

                if config.has_autosave or config.has_quicksave:
                    textbutton _("{#quick_page}A/Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()
