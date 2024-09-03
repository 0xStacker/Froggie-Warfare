//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./GreenFireBall.sol";

contract GoldenBullet is GreenFireBall{
    address purchaseToken;
    address qualifiedNft;
    uint immutable cost;
    constructor(string memory _name, string memory _symbol, address _purchaseToken, uint _cost) GreenFireBall(_name, _symbol){   
        purchaseToken = _purchaseToken;
        
        cost = _cost;
    }   

    error NotQualified();

    function claim(address _user) external override returns(bool){
        if(IERC721(qualifiedNft).balanceOf(_user) > 0){
            require(balanceOf(msg.sender) == 0, "Can only claim once");
            tokenId += 1;
            _mint(msg.sender, tokenId);         
            emit ClaimWeapon(name(), _user);
            return true;                                                                            
        }
        else{
            return false;
        }
    }

    function setQualifiedNft(address _nft) external onlyOwner{
        qualifiedNft = _nft;
    }

    function setPurchaseToken(address newToken) external onlyOwner{
        purchaseToken = newToken; 
    }

    // Purchase this weapon
    function purchaseWeapon(address _to) external returns (bool){
        // require(allowedTokens[_token], "Invalid Token");
        require(balanceOf(_to) == 0, "Can only purchase once");
        IERC20 token = IERC20(purchaseToken);
        bool call = token.transferFrom(_to, address(this), cost);
        if(call){
            tokenId += 1;
            _mint(_to, tokenId);
            emit PurchaseWeapon(name(), _to);
            return true;
        }
        else{
             return false;
        }
    }

    
    function getOwner() external view returns(address){
        return owner;
    }

    function getCost() external view returns(uint){
        return cost;
    }

     
    // function getPurchaseToken() external view returns(address){
    //     return purchase_token;
    // }
    
}