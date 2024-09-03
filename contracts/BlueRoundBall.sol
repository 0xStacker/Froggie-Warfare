//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./GoldenBullet.sol";

contract BlueRoundBall is GoldenBullet{

    constructor(string memory _name, string memory _symbol, address _purchaseToken, address _qualifiedNft, uint cost)
     GoldenBullet(_name, _symbol, _purchaseToken, cost){
        qualifiedNft = _qualifiedNft;
     }
     
}