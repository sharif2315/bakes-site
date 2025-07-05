import '../css/input.css';

import Alpine from "alpinejs";
import htmx from "htmx.org";
import collapse from '@alpinejs/collapse'
 

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.plugin(collapse)

Alpine.start();

// console.log('Hello from Vite!')