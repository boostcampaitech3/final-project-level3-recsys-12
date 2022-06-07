<img src="https://user-images.githubusercontent.com/57610590/172305396-0dfddf20-b132-4f2c-b5d2-7400abeae0e7.png"/>

<img src="https://user-images.githubusercontent.com/57610590/172306125-df20c616-c222-477b-bd50-3867c30673dd.png" alt="drawing" width="200"/> # LibraVerse

# LibraVerse
> GFM  Markdown and WYSIWYG Editor - Productive and Extensible

[![github release version](https://img.shields.io/github/v/release/nhn/tui.editor.svg?include_prereleases)](https://github.com/nhn/tui.editor/releases/latest) [![npm version](https://img.shields.io/npm/v/@toast-ui/editor.svg)](https://www.npmjs.com/package/@toast-ui/editor) [![license](https://img.shields.io/github/license/nhn/tui.editor.svg)](https://github.com/nhn/tui.editor/blob/master/LICENSE) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](https://github.com/nhn/tui.editor/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) [![code with hearth by NHN Cloud](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-NHN_Cloud-ff1414.svg)](https://github.com/nhn)

<img src="https://user-images.githubusercontent.com/37766175/121809054-446bac80-cc96-11eb-9139-08c6d9ad2d88.png" />


## 🚩 Table of Contents

- [Packages](#-packages)
- [Why TOAST UI Editor?](#-why-toast-ui-editor)
- [Features](#-features)
- [Examples](#-examples)
- [Browser Support](#-browser-support)
- [Pull Request Steps](#-pull-request-steps)
- [Contributing](#-contributing)
- [TOAST UI Family](#-toast-ui-family)
- [Used By](#-used-by)
- [License](#-license)


## 📦 Packages

### TOAST UI Editor

| Name | Description |
| --- | --- |
| [`@toast-ui/editor`](https://github.com/nhn/tui.editor/tree/master/apps/editor) | Plain JavaScript component |

### TOAST UI Editor's Wrappers

| Name | Description |
| --- | --- |
| [`@toast-ui/react-editor`](https://github.com/nhn/tui.editor/tree/master/apps/react-editor) | [React](https://reactjs.org/) wrapper component |
| [`@toast-ui/vue-editor`](https://github.com/nhn/tui.editor/tree/master/apps/vue-editor) | [Vue](https://vuejs.org/) wrapper component |

### TOAST UI Editor's Plugins

| Name | Description |
| --- | --- |
| [`@toast-ui/editor-plugin-chart`](https://github.com/nhn/tui.editor/tree/master/plugins/chart) | Plugin to render chart |
| [`@toast-ui/editor-plugin-code-syntax-highlight`](https://github.com/nhn/tui.editor/tree/master/plugins/code-syntax-highlight) | Plugin to highlight code syntax |
| [`@toast-ui/editor-plugin-color-syntax`](https://github.com/nhn/tui.editor/tree/master/plugins/color-syntax) | Plugin to color editing text |
| [`@toast-ui/editor-plugin-table-merged-cell`](https://github.com/nhn/tui.editor/tree/master/plugins/table-merged-cell) | Plugin to merge table columns |
| [`@toast-ui/editor-plugin-uml`](https://github.com/nhn/tui.editor/tree/master/plugins/uml) | Plugin to render UML |


## 🤖 Why TOAST UI Editor?

TOAST UI Editor provides **Markdown mode** and **WYSIWYG mode**. Depending on the type of use you want like production of *Markdown* or maybe to just edit the *Markdown*. The TOAST UI Editor can be helpful for both the usage. It offers **Markdown mode** and **WYSIWYG mode**, which can be switched any point in time.

### Productive Markdown Mode

![markdown](https://user-images.githubusercontent.com/37766175/121464762-71e2fc80-c9ef-11eb-9a0a-7b06e08d3ccb.png)

**CommonMark + GFM Specifications**

Today *CommonMark* is the de-facto *Markdown* standard. *GFM (GitHub Flavored Markdown)* is another popular specification based on *CommonMark* - maintained by *GitHub*, which is the *Markdown* mostly used. TOAST UI Editor follows both [*CommonMark*](http://commonmark.org/) and [*GFM*](https://github.github.com/gfm/) specifications. Write documents with ease using productive tools provided by TOAST UI Editor and you can easily open the produced document wherever the specifications are supported.

* **Live Preview** : Edit Markdown while keeping an eye on the rendered HTML. Your edits will be applied immediately.
* **Scroll Sync** : Synchronous scrolling between Markdown and Preview. You don't need to scroll through each one separately.
* **Syntax Highlight** : You can check broken Markdown syntax immediately.

### Easy WYSIWYG Mode

![wysiwyg](https://user-images.githubusercontent.com/37766175/121808381-251f5000-cc93-11eb-8c47-4f5a809de2b3.png)

* **Table** : Through the context menu of the table, you can add or delete columns or rows of the table, and you can also arrange text in cells.
* **Custom Block Editor** : The custom block area can be edited through the internal editor.
* **Copy and Paste** : Paste anything from browser, screenshot, excel, powerpoint, etc.

### UI
* **Toolbar** : Through the toolbar, you can style or add elements to the document you are editing.
![UI](https://user-images.githubusercontent.com/37766175/121808231-767b0f80-cc92-11eb-82a0-433123746982.png)

* **Dark Theme** : You can use the dark theme.
![UI](https://user-images.githubusercontent.com/37766175/121808649-8136a400-cc94-11eb-8674-812e170ccab5.png)

### Use of Various Extended Functions - Plugins

![plugin](https://user-images.githubusercontent.com/37766175/121808323-d8d41000-cc92-11eb-9117-b92a435c9b43.png)

CommonMark and GFM are great, but we often need more abstraction. The TOAST UI Editor comes with powerful **Plugins** in compliance with the Markdown syntax.

**Five basic plugins** are provided as follows, and can be downloaded and used with npm.

* [**`chart`**](https://github.com/nhn/tui.editor/tree/master/plugins/chart) : A code block marked as a 'chart' will render [TOAST UI Chart](https://github.com/nhn/tui.chart).
* [**`code-syntax-highlight`**](https://github.com/nhn/tui.editor/tree/master/plugins/code-syntax-highlight) : Highlight the code block area corresponding to the language provided by [Prism.js](https://prismjs.com/).
* [**`color-syntax`**](https://github.com/nhn/tui.editor/tree/master/plugins/color-syntax) : 
Using [TOAST UI ColorPicker](https://github.com/nhn/tui.color-picker), you can change the color of the editing text with the GUI.
* [**`table-merged-cell`**](https://github.com/nhn/tui.editor/tree/master/plugins/table-merged-cell) : 
You can merge columns of the table header and body area.
* [**`uml`**](https://github.com/nhn/tui.editor/tree/master/plugins/uml) : A code block marked as an 'uml' will render [UML diagrams](http://plantuml.com/screenshot).

## 🎨 Features

* [Viewer](https://github.com/nhn/tui.editor/tree/master/docs/en/viewer.md) : Supports a mode to display only markdown data without an editing area.
* [Internationalization (i18n)](https://github.com/nhn/tui.editor/tree/master/docs/en/i18n.md) : Supports English, Dutch, Korean, Japanese, Chinese, Spanish, German, Russian, French, Ukrainian, Turkish, Finnish, Czech, Arabic, Polish, Galician, Swedish, Italian, Norwegian, Croatian + language and you can extend.
* [Widget](https://github.com/nhn/tui.editor/tree/master/docs/en/widget.md) : This feature allows you to configure the rules that replaces the string matching to a specific `RegExp` with the widget node.
* [Custom Block](https://github.com/nhn/tui.editor/tree/master/docs/en/custom-block.md) : Nodes not supported by Markdown can be defined through custom block. You can display the node what you want through writing the parsing logic with custom block.

## 🐾 Examples

* [Basic](https://nhn.github.io/tui.editor/latest/tutorial-example01-editor-basic)
* [Viewer](https://nhn.github.io/tui.editor/latest/tutorial-example04-viewer)
* [Using All Plugins](https://nhn.github.io/tui.editor/latest/tutorial-example12-editor-with-all-plugins)
* [Creating the User's Plugin](https://nhn.github.io/tui.editor/latest/tutorial-example13-creating-plugin)
* [Customizing the Toobar Buttons](https://nhn.github.io/tui.editor/latest/tutorial-example15-customizing-toolbar-buttons)
* [Internationalization (i18n)](https://nhn.github.io/tui.editor/latest/tutorial-example16-i18n)

Here are more [examples](https://nhn.github.io/tui.editor/latest/tutorial-example01-editor-basic) and play with TOAST UI Editor!


## 🌏 Browser Support

| <img src="https://user-images.githubusercontent.com/1215767/34348387-a2e64588-ea4d-11e7-8267-a43365103afe.png" alt="Chrome" width="16px" height="16px" /> Chrome | <img src="https://user-images.githubusercontent.com/1215767/34348590-250b3ca2-ea4f-11e7-9efb-da953359321f.png" alt="IE" width="16px" height="16px" /> Internet Explorer | <img src="https://user-images.githubusercontent.com/1215767/34348380-93e77ae8-ea4d-11e7-8696-9a989ddbbbf5.png" alt="Edge" width="16px" height="16px" /> Edge | <img src="https://user-images.githubusercontent.com/1215767/34348394-a981f892-ea4d-11e7-9156-d128d58386b9.png" alt="Safari" width="16px" height="16px" /> Safari | <img src="https://user-images.githubusercontent.com/1215767/34348383-9e7ed492-ea4d-11e7-910c-03b39d52f496.png" alt="Firefox" width="16px" height="16px" /> Firefox |
| :---------: | :---------: | :---------: | :---------: | :---------: |
| Yes | 11+ | Yes | Yes | Yes |


## 🔧 Pull Request Steps

TOAST UI products are open source, so you can create a pull request(PR) after you fix issues. Run npm scripts and develop yourself with the following process.

### Setup

Fork `main` branch into your personal repository. Clone it to local computer. Install node modules. Before starting development, you should check if there are any errors.

```sh
$ git clone https://github.com/{your-personal-repo}/tui.editor.git
$ npm install
$ npm run build toastmark
$ npm run test editor
```

> TOAST UI Editor uses [npm workspace](https://docs.npmjs.com/cli/v7/using-npm/workspaces/), so you need to set the environment based on [npm7](https://github.blog/2021-02-02-npm-7-is-now-generally-available/). If subversion is used, dependencies must be installed by moving direct paths per package.

### Develop

You can see your code reflected as soon as you save the code by running a server. Don't miss adding test cases and then make green rights.

#### Run snowpack-dev-server
[snowpack](https://www.snowpack.dev/) allows you to run a development server without bundling.

``` sh
$ npm run serve editor
```




## 📜 License

This software is licensed under the [MIT](https://github.com/nhn/tui.editor/blob/master/LICENSE) © [NHN Cloud](https://github.com/nhn).


# Libraverse!

- 공공 도서관을 위한 메타버스 & 웹 도서 추천 시스템

## 1.프로젝트 개요

* 목적
    * 코로나로 인해 오프라인 도서관을 이용하기 힘들고, 책 추천 시스템이 있지만 통계 기반의 베스트셀러 위주의 책 추천이 이루어지고 있는 상황을 해결하여 시민들이 다시 도서관을 쉽게 접근할 수 있는 환경 구축

* 주요 기능
    * 개인 대출 이력에 기반한 도서 추천 시스템
    * 전저도서관 구축
    * 메타버스 구축 및 추천 결과 반영

## 2.Team

### RecSys_12조 Hi_Rec

#### 👨‍👩‍👦‍👦 Members  

권용훈|김정훈|정승환|최종현|한광석|
:-:|:-:|:-:|:-:|:-:
<img src='' height=80 width=80px></img>|<img src='' height=80 width=80px></img>|<img src='' height=80 width=80px></img>|<img src='' height=80 width=80px></img>|<img src='' height=80 width=80px></img>
[Github](https://github.com/Wingseter)|[Github](https://github.com/jj150618)|[Github](https://github.com/barobaro9842)|[Github](https://github.com/Jonghyunchoi94)|[Github](https://github.com/c0natus)

#### 🏆 Contribution  

- [`권용훈`](https://github.com/Wingseter) &nbsp; 역할 • 역할
- [`김정훈`](https://github.com/jj150618) &nbsp; 역할 • 역할
- [`정승환`](https://github.com/barobaro9842) &nbsp; 역할 • 역할
- [`최종현`](https://github.com/Jonghyunchoi94) &nbsp; 역할 • 역할
- [`한광석`](https://github.com/c0natus) &nbsp; 역할 • 역할

## 3.Tech Stack
<div>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=for-the-badge&logo=Pytorch&logoColor=white">
<img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/unrealengine-0E1128?style=for-the-badge&logo=unrealengine&logoColor=white"> 
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white">
/<div>
   
## 4. Dataset
https://nijianmo.github.io/amazon/index.html
   
## 5. Service Architecture
<img src="https://user-images.githubusercontent.com/57610590/172316403-8c10f61e-e3fc-4bb3-96b1-d2bd5936b4b2.png"/>
   
## 6. Web
<img src="https://user-images.githubusercontent.com/57610590/172314413-4cb9690a-7cd3-4cd6-ba45-9b3ca2f06225.png"/>

## 7. Metaverse
<img src="https://user-images.githubusercontent.com/57610590/172314340-0306095b-9556-4457-ac57-4ed20a5f9954.png"/> 
   
