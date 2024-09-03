//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";

interface IERC20{
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
}

contract GreenFireBall is ERC721{
    uint tokenId = 0;
    address immutable owner;
    mapping(address => bool) allowedTokens;
    mapping(address => uint) costInTokens;

    modifier onlyOwner{
        require(msg.sender == owner, "NotOwner");
        _;
    }

    event PurchaseWeapon(string weaponType, address _buyer);
    event ClaimWeapon(string weaponType, address _buyer);

    function addPurchaseToken(address tokenAddress, uint _costInToken) external onlyOwner{
        allowedTokens[tokenAddress] = true;
        costInTokens[tokenAddress] = _costInToken;
    }

    constructor(string memory _name, string memory _symbol) ERC721(_name, _symbol){
        owner = msg.sender;
    }    
    
    error Soulbound();

    function claim(address _user) external virtual returns(bool){
        require(balanceOf(_user) == 0, "Can only purchase once");
        tokenId += 1;
        _mint(_user, tokenId);
        emit ClaimWeapon(name(), _user);
        return true;
    }

    function approve(address, uint256) public virtual override{
        revert Soulbound();
    }

   
    function setApprovalForAll(address, bool) public virtual override{
        revert Soulbound();
    }

    function transferFrom(address, address, uint256) public virtual override {
        revert Soulbound();
     } 
    

    function safeTransferFrom(address, address, uint256, bytes memory) public virtual override{
        revert Soulbound();
    }


    function withdraw(address _token, address _to) external onlyOwner returns(bool){
        IERC20 token = IERC20(_token);
        uint balance = token.balanceOf(address(this));
        require(token.approve(_to, balance));
        require(token.transfer(_to, balance));
        return true;
    }

}
