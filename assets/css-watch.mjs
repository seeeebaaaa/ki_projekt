import * as esbuild from 'esbuild'
import path from 'path'

const isProd = process.env.NODE_ENV === 'production'

const sourceEntry = path.resolve('css/app.css') // Entry CSS

const buildOptions = {
  entryPoints: [sourceEntry],
  bundle: true,
  outdir: '../public/css',
  loader: { '.css': 'css' },
  minify: isProd,
  sourcemap: !isProd,
  logLevel: 'info',
  loader: {
    '.png': 'file',
    '.jpg': 'file',
    '.gif': 'file',
    '.svg': 'file',
    '.eot': 'file',
    '.ttf': 'file',
    '.woff': 'file',
    '.woff2': 'file',
    '.css': 'css',
  },
  publicPath: "/css/",
  assetNames: 'assets/[name]-[hash]', 
  external: ["images/*"]
}

async function start() {
  try {
    const ctx = await esbuild.context(buildOptions)

    if (!isProd) {
      await ctx.watch()
      console.log('👀 Watching CSS for changes...')
    } else {
      await ctx.rebuild()
      await ctx.dispose()
      console.log('✅ CSS built for production')
    }
  } catch (err) {
    console.error('❌ CSS build failed:', err)
    process.exit(1)
  }
}

start()
