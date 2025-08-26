import { LitElement, html, css, cache } from '@lit';
import { ContextConsumer } from '@lit/context';

import { contextOptions } from './data-context.js';


// Card to display item info, in different modes
export default class ItemCard extends LitElement {
    _consumer = new ContextConsumer(this, contextOptions);

    get data() {
        return this._consumer.value;
    }

    static properties = {
        mode: {},   // Card display mode
        name: {},   // Item name
    }

    static styles = css`
        .item-card.icon,
        .item-card.compact {
            display: flex;
            align-items: center;
            gap: 0.25em;
        }
    `

    static validModes = ['icon', 'compact', 'detailed'];

    get mode() {
        return this._mode;
    }

    set mode(value) {
        if (ItemCard.validModes.includes(value))
            this._mode = value;
        else
            console.error(`Invalid mode for item-card: ${value}`);
    }

    constructor() {
        super();

        this.mode = 'compact';
        this.name = null;
    }

    // Currently displayed item
    get item() {
        return this.data?.items[this.name];
    }

    icon(size=24) {
        let filename = this.item?.icon ?? "Icon_Warning.png";

        return html`<img src="images/${filename}" alt=${this.name} title=${this.name} width=${size} height=${size}>`;
    }

    // Just an icon
    iconMode() {
        return html`
            <div class="item-card icon" title=${this.name}>${cache(this.icon())}</div>
        `;
    }

    // Icon and name
    compactMode() {
        return html`
            <div class="item-card compact" title=${this.name}>${cache(this.icon())} ${this.name}</div>
        `;
    }

    // Full-on item card
    detailedMode() {
        let tags = this.item?.tags?.join(', ') ?? '';

        return html`
            <div class="item-card detailed" title=${this.name}>
                <div>${cache(this.icon(32))} <h3>${this.name}</h3></div>
                <div>${tags}</div>
            </div>
        `;
    }

    render() {
        return this[this.mode + 'Mode']();
    }
}

customElements.define('item-card', ItemCard)
