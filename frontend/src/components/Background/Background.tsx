import styled from 'styled-components';
import {useBlurableImage} from 'hooks';
import {WaveBottom} from 'assets';
import {colors} from 'styles';

interface IBackground {
  fullImage: string;
  smallImage?: string;
  withWave?: boolean;
}

const Wrapper = styled.div`
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: -1;
  overflow: hidden;
`;
const Image = styled.div<{blur: boolean; src: string}>`
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 100%;
  height: 100%;
  filter: ${(p) => (p.blur ? 'blur(10px)' : 'none')};
  background: url(${(p) => p.src}) no-repeat center center fixed,
    ${colors.gradientPurpleOrange};
  background-size: cover;
  transform: scale(1.05);
`;

const Wave = styled.img.attrs({src: WaveBottom, alt: 'Wave'})`
  width: 100%;
`;

export function Background({
  fullImage,
  smallImage = fullImage,
  withWave = false,
}: IBackground) {
  const {src, blur} = useBlurableImage(fullImage, smallImage);

  return (
    <Wrapper>
      <Image src={src} blur={blur}>
        {withWave ? <Wave /> : null}
      </Image>
    </Wrapper>
  );
}
