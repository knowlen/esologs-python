/**
 * Initialize Mermaid for diagram rendering
 */
document.addEventListener('DOMContentLoaded', function() {
    if (window.mermaid) {
        mermaid.initialize({
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {
                // Vim-style colors for mermaid diagrams
                primaryColor: '#5f5f87',
                primaryTextColor: '#d0d0d0',
                primaryBorderColor: '#585858',
                lineColor: '#87ceeb',
                secondaryColor: '#444444',
                tertiaryColor: '#303030',
                background: '#1c1c1c',
                mainBkg: '#262626',
                secondBkg: '#303030',
                tertiaryBkg: '#1c1c1c',
                textColor: '#d0d0d0',
                labelTextColor: '#d0d0d0',
                nodeBorder: '#585858',
                clusterBkg: '#303030',
                clusterBorder: '#585858',
                defaultLinkColor: '#87ceeb',
                edgeLabelBackground: '#1c1c1c',
                nodeTextColor: '#d0d0d0'
            }
        });
    }
});
