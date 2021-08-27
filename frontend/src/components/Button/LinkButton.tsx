import {AnchorHTMLAttributes, DetailedHTMLProps} from 'react';
import styled from 'styled-components';
import {Link} from '@uitk/react';
import {NewWindow} from '@uitk/react-icons';
import {theme} from 'styles';

const StyledLink = styled(Link)`
  ${(p) =>
    p.bold
      ? `
font-size: ${theme.fontSizeH5};
  font-family: ${theme.fontFamilyH5};
  font-weight: ${theme.fontWeightH5};
`
      : null}
  line-height: 1.5;
  color: ${theme.colorTextLink};
  display: inline-flex;
  align-items: center;
`;

const Icon = styled(NewWindow).attrs(() => ({
  fill: theme.colorTextLink,
}))`
  height: ${theme.spacingSM};
  width: ${theme.spacingSM};
  margin-left: ${theme.spacingXXS};
`;
interface ILinkButton
  extends DetailedHTMLProps<
    AnchorHTMLAttributes<HTMLAnchorElement>,
    HTMLAnchorElement
  > {
  external?: boolean;
  bold?: boolean;
}
export function LinkButton({
  external = true,
  bold = false,
  href = '',
  children,
  ...props
}: ILinkButton) {
  return (
    <StyledLink
      href={href}
      target={external ? '_blank' : '_self'}
      bold={bold}
      {...props}>
      {children}
      {external ? <Icon /> : null}
    </StyledLink>
  );
}
