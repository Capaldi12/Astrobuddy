import { LitElement, html, css } from '@lit';


// Named panel for content
export default class ContentPanel extends LitElement {
    static properties = {
        title: {}
    }

    static styles = css`
        /* A bit of magic to make navigation work properly */
        .offset {
            border-top: 87px solid transparent;
            margin-top: -87px;
        }

        .title-bar {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .title {
            width: fit-content;
            color: var(--text-secondary);
            font-weight: bold;
            white-space: nowrap;
        }

        .line {
            width: 100%;
            height: 1px;
            border-bottom: 2px solid var(--text-secondary);
        }
    `

    constructor() {
        super();
        this.title = "Section";
    }

    render() {
        return html`
            <div class="offset">
                <div class="title-bar">
                    <div class="title">${this.title}</div>
                    <div class="line"></div>
                </div>
                <slot></slot>
            </div>
        `;
    }
}

customElements.define('content-panel', ContentPanel);
