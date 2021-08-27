import {PropsWithChildren} from 'react';
import styled from 'styled-components';
import {theme} from 'styles';

type TWrapperVariant = 'circle';

const Outer = styled.div<{
  variant: TWrapperVariant;
}>`
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: ${theme.colorBackgroundSelected};
  height: 3rem;
  width: 3rem;
  ${(p) => (p.variant === 'circle' ? 'border-radius: 100%;' : null)}
  margin-right: ${theme.spacingXS};
`;

interface IIconWrapper {
  variant?: TWrapperVariant;
}

export function IconWrapper({
  children,
  variant = 'circle',
}: PropsWithChildren<IIconWrapper>) {
  return <Outer variant={variant}>{children}</Outer>;
}
