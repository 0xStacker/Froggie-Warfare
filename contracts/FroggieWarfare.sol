//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC721{
    function balanceOf(address owner) external view returns (uint256 balance);
    function claim(address _user) external returns(bool);
    function purchaseWeapon(address _to) external returns(bool);
    function name() external view returns (string memory);
    function mint(address _to) external; 
    function getCost() external view returns(uint);
}

interface IERC20{
    function approve(address spender, uint256 value) external returns (bool);
    function mint(address _to) external;
}

contract FroggieWarfare{
    address private owner;
    address internal purchase_token;
    address qualifiedNft;
    address private manager;
    mapping (address => bool) users;
    mapping(address => string) public userCred;
    mapping(address => uint) public scores;
    mapping(address => bool) internal weaponCheck;
    mapping(address => address[]) internal userWeapons;
    address defaultWeapon;
    address[] internal weapons;
    mapping(address => string) internal weaponNames;
    string internal name;


    constructor(address _manager, address _defaultWeapon, address _purchaseToken, address _qualifiedNft){
        owner = msg.sender;
        manager = _manager;
        qualifiedNft = _qualifiedNft;
        purchase_token = _purchaseToken;
        defaultWeapon = _defaultWeapon;
        weapons.push(defaultWeapon);
        IERC721 weapon = IERC721(_defaultWeapon);
        name = weapon.name();
        weaponNames[defaultWeapon] = name;
    }
    

    event ClaimWeapon(address weaponAddress, string weaponName);
    event AddNewWeapon(address weaponAddress);
    event RegisterUser(address userAddress);
    event PurchaseWeapon(address weaponAddress, string weaponName);


    modifier onlyOwner{
        require(msg.sender == owner, "Not Owner");
        _;

    }

    modifier onlyManager{
        require(msg.sender == manager, "Not Manager");
        _;
    }

    modifier onlyUsers{
        require(users[msg.sender], "Not Registered");
        _;
    }


    error CannotClaim(address weaponAddress);
    error CannotPurchase(address weaponAddress);


    function setTestToken(address newToken) external onlyOwner{
        purchase_token = newToken;
    }

    function setQualifiedNft(address _newNft) external onlyOwner{
        qualifiedNft = _newNft;
    }

// Mint test token for purchasing weapon
    function mintTestToken() external {
        IERC20 token = IERC20(purchase_token);
        token.mint(msg.sender);
    }


    function claimWeapon(address _weapon) public{
        IERC721 weapon = IERC721(_weapon);
        bool call = weapon.claim(msg.sender);
        if(call){
            userWeapons[msg.sender].push(_weapon);
            emit ClaimWeapon(_weapon, weaponNames[_weapon]);
        }
        else{
            revert CannotClaim(_weapon);
        }
        
    }

    function mintTestNft() external {
        IERC721 nft = IERC721(qualifiedNft);
        nft.mint(msg.sender);
    }

// Add new weapon to the game
    function addNewWeapon(address _weapon) external onlyOwner{
        weapons.push(_weapon);
        weaponCheck[_weapon] = true;
        name = IERC721(_weapon).name();
        weaponNames[_weapon] = name;
        emit AddNewWeapon(_weapon);
    }

// Register new player
    function register(string memory passwordHash) external{
        require(users[msg.sender] == false);
        userCred[msg.sender] = passwordHash;
        users[msg.sender] == true;
        claimWeapon(defaultWeapon);
        emit RegisterUser(msg.sender);
    }

   
// All weapons held by a user
    function getUserWeapons(address user) external view returns(address[] memory){
        return userWeapons[user];
    }

// Cost of weapon
    function getWeaponCost(address weaponAddress) external view returns(uint){
        require(weaponCheck[weaponAddress] == true);
        IERC721 weapon = IERC721(weaponAddress);
        uint cost = weapon.getCost();
        return cost;
    }

// Buy weapon
    function purchaseWeapon(address weaponAddress) external{
        require(weaponCheck[weaponAddress] == true, "NotAWeapon");
        IERC721 weapon = IERC721(weaponAddress);
        uint cost = weapon.getCost();
        (bool success, ) = purchase_token.delegatecall(abi.encodeWithSignature("approve(address, uint256)", weaponAddress, cost));
        bool call = weapon.purchaseWeapon(msg.sender);
        success;
        if (call){
            userWeapons[msg.sender].push(weaponAddress);
            emit PurchaseWeapon(weaponAddress, weaponNames[weaponAddress]);
        }
        else{
            revert CannotPurchase(weaponAddress);
        }
    }

    function getCred(address user) external view returns(string memory){
        return userCred[user];
    }

    function availableWeapons() external view returns(address[] memory){
        return weapons;
    }

    function getWeaponNameByAddress(address _weaponAddress) external view returns(string memory){
        return weaponNames[_weaponAddress];
    }


 
}
