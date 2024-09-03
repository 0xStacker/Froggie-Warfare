//SPDX-License-Identifier: MIT
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";
pragma solidity ^0.8.0;

contract Croak is ERC20("CROACK", "CROACK"){
    function mint(address _to) external{
        _mint(_to, 1000 * 10**18);
    }
}
