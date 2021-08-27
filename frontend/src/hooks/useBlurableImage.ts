import {useState, useEffect} from 'react';

export function useBlurableImage(fullImage: string, smallImage: string) {
  const [src, setSrc] = useState(smallImage);

  useEffect(() => {
    setSrc(smallImage);
    const img = new Image();
    img.src = fullImage;
    img.onload = () => {
      setSrc(fullImage);
    };
  }, [smallImage, fullImage]);

  return {
    src,
    blur: src === smallImage,
  };
}
