//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
contract testEfrog is ERC721("EFROG", "EFROG"){
    uint tokenId = 0;

    function mint(address _to) external{
        tokenId += 1;
        _mint(_to, tokenId);
    }
}