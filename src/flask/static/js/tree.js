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

  // Step 2: Recursively build HTML using jQuery
  function createTree (obj) {
    const $section = $('<ul></ul>')
    for (const key in obj) {
      const $li = $('<li></li>')
      if (obj[key] === null) {
        $li.html($('<div>' + key + '</div>').addClass('element')) // file
        $li.addClass('file')
      } else {
        const $details = $('<details></details>')
        const $summary = $('<summary></summary>')
          .html($('<div>' + key + '</div>').addClass('element'))
          .addClass('folder')
        $details.append($summary)
        $details.append(createTree(obj[key]))
        $li.append($details)
      }
      $section.append($li)
    }
    return $section
  }
  async function cT (tree, $root) {
    for (const key in tree) {
      if (tree[key] === null) {
        // key is a file, so add leaf to root
        const $checkbox = $('<div></div>')
          .addClass('checkbox')
          .append($('<input type="checkbox" name="" id="" ></input>'))
        $root.append(
          $('<div></div>')
            .addClass('leaf item')
            .append(
              $('<div></div>')
                .addClass('symbol')
                .html(await getSVG('page.svg'))
            )
            .append($('<div></div>').addClass('name').text(key))
            .append($checkbox)
        )
      } else {
        // key is a folder, so start new section adn append that to the root
        const $section = $('<div></div>').addClass('section')
        const $head = $('<div></div>')
          .addClass('head item')
          .append(
            $('<div></div>')
              .addClass('action')
              .html(await getSVG('plus.svg'))
          )
          .append(
            $('<div></div>')
              .addClass('symbol')
              .html(await getSVG('folder.svg'))
          )
          .append($('<div></div>').addClass('name').text(key))
        const $checkbox = $('<div></div>')
          .addClass('checkbox')
          .append($('<input type="checkbox" name="" id="" ></input>'))
        const $group = $('<div></div>')
          .addClass('group')
          .append('<div class="line"><div></div></div>')
        const $items = $('<div></div>').addClass('items')

        $section.append($head)
        $head.append($checkbox)
        $group.append($items)
        $section.append($group)
        await cT(tree[key], $items)
        $root.append($section)
      }
    }
    return $root
  }

  return await cT(root, $('<div></div>').addClass('tree'))
}

async function getSVG (svgName) {
  r = await fetch('/static/svg/' + svgName)
  return await r.text()
}

async function load_tree (paths) {
  tree = await buildTree(paths)
  $('.main>.content>.files').html(tree)
}
