import * as esbuild from 'esbuild'
import copyStaticFiles from 'esbuild-copy-static-files'

let minify = false
let sourcemap = true
let watch = true

if (process.env.NODE_ENV === 'production') {
  minify = true
  sourcemap = false
  watch = false
}

const config = {
  entryPoints: ['./js/app.js', './js/test.js'],
  outdir: '../public/js',
  bundle: true,
  minify: minify,
  sourcemap: sourcemap,
  plugins: [copyStaticFiles()],
  splitting: true,
  format: 'esm',
  // loader: {
  //   '.png': 'file',
  //   '.jpg': 'file',
  //   '.gif': 'file',
  //   '.svg': 'file',
  //   '.eot': 'file',
  //   '.ttf': 'file',
  //   '.woff': 'file',
  //   '.woff2': 'file',
  //   '.css': 'css',
  // },
  // publicPath: "/js/",
  inject: ["js/inject-jquery.js"],
  // assetNames: 'assets/[name]-[hash]', // adjust to match your public asset path
};

if (watch) {
  let context = await esbuild.context({...config, logLevel: 'info'})
  await context.watch()
} else {
  esbuild.build(config)
}
