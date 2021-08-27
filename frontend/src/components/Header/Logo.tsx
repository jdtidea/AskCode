import styled from 'styled-components';
import {LogoInverse} from 'assets';

const LogoImage = styled.img.attrs(() => ({
  src: LogoInverse,
  alt: 'Ask Optum',
}))`
  width: 110px;
  margin-top: 10px;
`;
const LogoWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;

export function Logo() {
  return (
    <LogoWrapper>
      <a href="/">
        <LogoImage />
      </a>
    </LogoWrapper>
  );
}
