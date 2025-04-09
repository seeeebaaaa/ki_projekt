import $ from 'jquery'

async function buildTree (paths) {
    const root = {}

    // Step 1: Build nested object structure
    paths.forEach(path => {
        const parts = path.split('/')
        let current = root
        parts.forEach((part, i) => {
            if (!current[part]) {
                current[part] = i === parts.length - 1 ? null : {}
            }
            current = current[part]
        })
    })

    async function cT (tree, $root, path_til_now) {
        for (const key in tree) {
            if (tree[key] === null) {
                // key is a file, so add leaf to root
                const $checkbox = await buildCheckbox(path_til_now,key)
                $root.append(
                    $('<div></div>')
                        .addClass('leaf item')

                        .attr('path', path_til_now + '/' + key)
                        .append(
                            $('<div></div>')
                                .addClass('symbol')
                                .html(await getSVG('page.svg'))
                                .on('click', open_file)
                        )
                        .append(
                            $('<div></div>')
                                .addClass('name')
                                .text(key)
                                .on('click', open_file)
                        )
                        .append($checkbox)
                )
            } else {
                // key is a folder, so start new section adn append that to the root
                const $section = $('<div></div>').addClass('section')
                const $head = $('<div></div>')
                    .addClass('head item')
                    .attr('path', path_til_now + '/' + key)
                    .append(
                        $('<div></div>')
                            .addClass('action')
                            .html(await getSVG('plus.svg'))
                            .on('click', unfold_section)
                    )
                    .append(
                        $('<div></div>')
                            .addClass('symbol')
                            .html(await getSVG('folder.svg'))
                            .on('click', unfold_section)
                    )
                    .append(
                        $('<div></div>')
                            .addClass('name')
                            .text(key)
                            .on('click', unfold_section)
                    )
                const $checkbox = await buildCheckbox(path_til_now,key)
                const $group = $('<div></div>')
                    .addClass('group')
                    .append('<div class="line"><div></div></div>')
                const $items = $('<div></div>').addClass('items')

                $section.append($head)
                $head.append($checkbox)
                $group.append($items)
                $section.append($group)
                await cT(tree[key], $items, path_til_now + '/' + key)
                $root.append($section)
            }
        }
        return $root
    }

    return await cT(root, $('<div></div>').addClass('tree'), '')
}

const buildCheckbox = async (path_til_now, key) => {
  const $checkbox = $('<div></div>')
                    .addClass('checkbox')
                    .append($(`<input type="checkbox" name="" id="cb-${(path_til_now + '/' + key).replaceAll("/","-")}" ></input>`).hide())
                    .append($(`<label for="cb-${(path_til_now + '/' + key).replaceAll("/","-")}"></label>`).html(await getSVG('star.svg')))
  return $checkbox
}
  

const stored_images = {}

async function getSVG (svgName) {
    // check if already loaded for performance
    if (stored_images[svgName]) return stored_images[svgName]

    const r = await fetch('svg/' + svgName)
    const text = await r.text()
    stored_images[svgName] = text
    return text
}

export async function load_tree (paths) {
    const tree = await buildTree(paths)
    $('.main>.content>.files>.none').hide()
    $('.main>.content>.files>.tree').remove()
    $('.main>.content>.files').append(tree)
}

window.load_tree = load_tree

// tree functions

const unfold_section = e => {
    const head_item = $(e.currentTarget).closest('.head.item')
    head_item.siblings().toggleClass('open')
}

const open_file = e => {
    const item = $(e.currentTarget).closest('.leaf.item')
    console.log(`Request file from server.. (${item.attr('path')})`)
}
