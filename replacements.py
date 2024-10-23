import re


def replace_variables(content, vars):
    # Regular expression to remove <Default ¶ Font\>

    # content = re.sub(
    #     r'(<VariableDef\s*`<Default ¶ Font\\>)(.*?)',
    #     r"<VariableDef \2",
    #     content
    # )

    content = re.sub(
        r'(<VariableDef\s*`<Default ¶ Font\\>)(.*?)\'',
        r"<VariableDef `\2'",
        content
    )

    content = re.sub(
        r'<TblColumnWidth\s*2\.89033\s*cm>\s*<TblColumnWidth\s*2\.49553\s*cm>\s*<TblColumnWidth\s*2\.32456\s*cm>\s*<TblColumnWidth\s*2\.49553\s*cm>\s*<TblColumnWidth\s*2\.32456\s*cm>\s*<TblColumnWidth\s*2\.51262\s*cm>\s*<TblColumnWidth\s*2\.51263\s*cm>',
        '<TblColumnWidth 2.797 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>',
        content
    )

    content = re.sub(
        r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.16131\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>',
        '  <TblColumnWidth 10.175 cm>\n  <TblColumnWidth 2.46 cm>\n  <TblColumnWidth 4.919 cm>',
        content
    )


    content = re.sub(
        r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.16131\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>',
        '<TblColumnWidth 10.175 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 4.919 cm>',
        content
    )


    content = re.sub(
        r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.14069\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>',
        '<TblColumnWidth 10.175 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 4.919 cm>',
        content
    )


    content = re.sub(
        r'<TblColumnWidth\s*2\.7968\s*cm>\s*<TblColumnWidth\s*2\.51114\s*cm>\s*<TblColumnWidth\s*2\.3391\s*cm>\s*<TblColumnWidth\s*2\.51114\s*cm>\s*<TblColumnWidth\s*2\.3391\s*cm>\s*<TblColumnWidth\s*2\.52834\s*cm>\s*<TblColumnWidth\s*2\.52834\s*cm>',
        '<TblColumnWidth 2.797 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>',
        content
    )


    content = re.sub(
        r'(<VariableFormat\s*>\s*<VariableName\s*`TIMLeadOfficeReleasedRD\'?>\s*<VariableDef\s*`)(NE1)(\'?>\s*>)',
        r"\1'>\n>",
        content
    )

    content = re.sub(
        r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.12327\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>',
        '<TblColumnWidth 10.175 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 4.919 cm>',
        content
    )


    content = re.sub(
        r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.13485\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>',
        '<TblColumnWidth 10.175 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 4.919 cm>',
        content
    )


    # Replace SCHKA1Number
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`SCHKA1Number\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['KaNumber']}'>", content)

    # Replace SCHKA2Number to SCHKA7Number with empty values
    for i in range(2, 8):
        content = re.sub(
            fr'(<VariableFormat\s*<VariableName\s*`SCHKA{i}Number\'?>\s*<VariableDef\s*`)(.*?)(\'?>)',
            r"\1'>", content)

    # Replace SCHKA1Date
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`SCHKA1Date\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['KaDate']}'>", content)

    # Replace SCHKA2Date to SCHKA7Date with empty values
    for i in range(2, 8):
        content = re.sub(
            fr'(<VariableFormat\s*<VariableName\s*`SCHKA{i}Date\'?>\s*<VariableDef\s*`)(.*?)(\'?>)',
            r"\1'>", content
        )

    # Replace SCHKA1Version
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`SCHKA1Version\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['KaVersion']}'>", content)

    # Replace SCHKA2Version to SCHKA7Version with empty values
    for i in range(2, 8):
        content = re.sub(
            fr'(<VariableFormat\s*<VariableName\s*`SCHKA{i}Version\'?>\s*<VariableDef\s*`)(.*?)(\'?>\s*>)',
            r"\1'>\n >", content)

    # Replace SCHDateReleased
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`SCHDateReleased\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['deliveryDate']}'>", content)

    # Replace SCHDateReleased
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`TIMDateReleasedRD\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['deliveryDate']}'>", content)


    # Replace SCHNameReleased
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`TIMNameReleasedRD\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['KaNameReleased']}'>", content)

    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`SCHNameReleased\'?>\s*<VariableDef\s*)(`.*?)(\'?>)',
        rf"\1`{vars['KaNameReleased']}'>", content)

    # Check for Restriction_{vars['languageCode']}
    # restriction_pattern = rf"Restriction_{vars['languageCode']}"
    restriction_pattern = rf"Titlepage_Translation_{vars['languageCode']}"

    print(restriction_pattern)
    print(re.search(restriction_pattern, content))
    if re.search(restriction_pattern, content):
        # Check if <PageBackground `75'>
        if re.search(r'<PageBackground\s*`75\'?>', content):
            # Replace <PageBackground `75'> with new value
            content = re.sub(
                r'(<PageBackground\s*`)(75)(\'?>)',
                rf"\1Restriction_{vars['languageCode']}'>", content)
                # rf"\1Titlepage_Translation_{vars['languageCode']}'>", content)
        else:
            print("Unfortunately, we are running a longer scenario. Replacing <PageBackground> only for <PageNum `2'>")
            content = re.sub(
                r'(<PageNum\s*`2\'[\s\S]*?<PageBackground\s*`)(.*?)\'',
                rf"\1Restriction_{vars['languageCode']}'>", content)
                # rf"\1Titlepage_Translation_{vars['languageCode']}'>", content)
    else:
        print(f"Fragment Restriction_{vars['languageCode']} not found in the document. Skipping this code fragment.")

    # Clear SCHLeadOffice
    content = re.sub(
        r'(<VariableName\s*`SCHLeadOffice\'?>\s*<VariableDef\s*`)(.*?)\'',
        r"\1'", content)

    # Replace TIMDocNumber
    content = re.sub(
        r'(<VariableFormat\s*<VariableName\s*`TIMDocNumber\'?>\s*<VariableDef\s*`\d+)(\'?>)',
        rf"\1_{vars['languageCode']}'>", content)

    # Replace TblColumnWidth
    content = re.sub(
        r'<TblColumnWidth\s*14\.23654\s*cm>\s*<TblColumnWidth\s*2\.881\s*cm>\s*<TblColumnWidth\s*2\.881\s*cm>',
        '<TblColumnWidth 11.363 cm>\n<TblColumnWidth 2.881 cm>\n<TblColumnWidth 5.76 cm>',
        content
    )

    # Replace TblColumnWidth Portaint version 1
    content = re.sub(
        r'<TblColumnWidth\s*11\.93173\s*cm>\s*<TblColumnWidth\s*2\.12504\s*cm>\s*<TblColumnWidth\s*3\.505\s*cm>',
        '<TblColumnWidth 10.175 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 4.919 cm>',
        content
    )



        # Replace TblColumnWidth Portaint version 2
    content = re.sub(
        r'<TblColumnWidth\s*2\.81372\s*cm>\s*<TblColumnWidth\s*2\.51114\s*cm>\s*<TblColumnWidth\s*2\.3391\s*cm>\s*<TblColumnWidth\s*2\.51114\s*cm>\s*<TblColumnWidth\s*2\.3391\s*cm>\s*<TblColumnWidth\s*2\.52834\s*cm>\s*<TblColumnWidth\s*2\.52834\s*cm>',
        '<TblColumnWidth 2.797 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>\n<TblColumnWidth 2.46 cm>',
        content
    )

    content = re.sub(r'[„“]', '"', content)


    return content
