export class IconModel {
    srcImg: string;
    srcImgHover: string;
    currentImage: string;
    onClickFunction: Function | undefined;

    constructor(srcImg: string, srcImgHover: string, onClickFunction: Function | undefined) {
        this.srcImg = srcImg;
        this.srcImgHover = srcImgHover;
        this.onClickFunction = onClickFunction;
        this.currentImage = srcImg;
    }
}