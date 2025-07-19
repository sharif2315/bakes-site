import '../css/input.css';

import Alpine from "alpinejs";
import htmx from "htmx.org";
import collapse from '@alpinejs/collapse'
import focus from '@alpinejs/focus'

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.plugin(collapse);
Alpine.plugin(focus);

Alpine.start();