import './MemberLink.scss';
import styled from 'styled-components';
import {Text} from '@uitk/react';
import React, {useState} from 'react';
import {HelperText, Label, TextInput, Button} from '@uitk/react';
import {MemberImage, GroupImage} from 'assets';
import {MsGraphService} from 'helpers';
import {Dialog} from '@uitk/react';

export function MemberLink() {
  const [dateValue, setdateValue] = useState<string>('');
  const [memberValue, setMemberValue] = useState<string>('');
  const [customerValue, setCustomerValue] = useState<string>('');

  const [isOpen, setIsOpen] = useState<boolean>(false);

  const dismiss = () => setIsOpen(false);

  const onChange = (event) => {
    setdateValue(event.target.value);
  };

  const onMemberValueChange = (event) => {
    setMemberValue(event.target.value);
  };

  const onCustomerValueChange = (event) => {
    setCustomerValue(event.target.value);
  };

  const VisuallyHidden = styled.span`
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    height: 1px;
    overflow: hidden;
    position: absolute;
    white-space: nowrap;
    width: 1px;
  `;

  const onSaveBtnClicked = async () => {
    updateUser();
  };

  const updateUser = async () => {
    // let updateUser = {
    //     preferredLanguage : memberValue,
    //     officeLocation : customerValue,
    //     jobTitle : dateValue,
    // }
    let updateUser = {
      extension_f3fb518578a34f3fb90c54fd4c3eee46_MemberID: memberValue,
      extension_f3fb518578a34f3fb90c54fd4c3eee46_GroupNumber: customerValue,
      extension_f3fb518578a34f3fb90c54fd4c3eee46_DateofBirth: dateValue,
    };
    let _result = await MsGraphService.update(updateUser).catch((e) => {
      console.log('ERROR at Results page ', e);
      return;
    });

    setIsOpen(false);
    console.log('----------', _result);
  };
  return (
    <>
      <span>
        Don't see the answer? <b>Link your healthcare information</b> to unlock
        the power of AskOptum!
        <br />
        <span className="sub-text">
          you can always link your account later on the profile page
        </span>
        <Button onPress={() => setIsOpen(true)} className="link-btn">
          <span>Link</span>
          <VisuallyHidden>Opens Modal Window</VisuallyHidden>
        </Button>
      </span>

      {isOpen && (
        <Dialog
          isOpen={isOpen}
          title="Link your information"
          closeButtonText="X"
          isDismissable
          className="dialog-member-link"
          onClose={dismiss}>
          <Dialog.Body>
            <Text>
              <br />
              <span className="sub-text">
                By linking your healthcare information, Optum can provide you
                with better aswers faster than ever!
              </span>
              <span className="sub-text">
                This enables us to gather information on your behalf from across
                the enterprise.
              </span>

              <form className="align">
                <div className="row">
                  <div className="col-4">
                    <Label style={{display: 'flex'}}>Member ID</Label>
                    <TextInput
                      value={memberValue}
                      onChange={onMemberValueChange}
                    />
                  </div>
                  <div className="col-4">
                    <img className="demo-img" alt="Member" src={MemberImage} />
                  </div>
                </div>
                <div className="row">
                  <div className="col-4">
                    <Label style={{display: 'flex'}}>Group Number</Label>
                    <TextInput
                      value={customerValue}
                      onChange={onCustomerValueChange}
                    />
                  </div>
                  <div className="col-4">
                    <img className="demo-img" alt="Group" src={GroupImage} />
                  </div>
                </div>
                <div className="row">
                  <div className="col-3">
                    <div className="date-input-holder">
                      <Label style={{display: 'flex'}}>Date Of Birth</Label>
                      <HelperText style={{display: 'flex'}}>
                        MM/DD/YYYY
                      </HelperText>
                      <TextInput value={dateValue} onChange={onChange} />
                    </div>
                  </div>
                </div>
              </form>
            </Text>
          </Dialog.Body>
          <Dialog.Actions>
            <Button onPress={onSaveBtnClicked}>Save & link</Button>
            <Button variant="ghost" onPress={dismiss}>
              Cancel
            </Button>
          </Dialog.Actions>
        </Dialog>
      )}
    </>
  );
}
